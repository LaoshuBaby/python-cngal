import os
import time
from datetime import datetime

import networkx as nx

from pycngal.const import api_endpoint, db_name, type_code
from pycngal.database import (
    init_collection,
    init_connection,
    insert_entry,
    select_entry,
    unify_select_entry,
    update_entry,
)
from pycngal.network import no_proxy, request_swagger_api


def type2collection(type: int) -> str:
    return type_code[type]


def print_time(fn):
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = fn(*args, **kwargs)
        time_end = time.time()
        message = "[TIME.{fn_name}]: {duration}s".replace(
            "{fn_name}", fn.__name__
        ).replace("{duration}", str(round((time_end - time_start), 3)))
        print(message)
        return result

    return wrapper


def init_graph():
    @print_time
    def get_entry_meta_list() -> dict:
        return request_swagger_api("/api/entries/GetAllEntriesIdName")

    def get_entry_data(entry_meta_list, max_limit):
        for entry_meta in entry_meta_list:
            id = entry_meta["id"]
            if id <= max_limit:

                @print_time
                def maintain(id):
                    # fetch
                    def get_data_fetch() -> dict:
                        time_start = time.time()
                        entry = request_swagger_api(
                            "/api/entries/GetEntryView/{id}".replace(
                                "{id}", str(id)
                            )
                        )
                        time_end = time.time()
                        flag_detailed_time = False
                        if flag_detailed_time == True:
                            print(
                                "[TIME.get_entry.{id}]: {time}s".replace(
                                    "{id}", str(id)
                                ).replace(
                                    "{time}",
                                    str(round((time_end - time_start), 3)),
                                )
                            )
                        return entry

                    # insert
                    def insert(entry):
                        post_id = insert_entry(
                            entry=entry,
                            db_name=db_name,
                            collection_name="cngal."
                            + type2collection(entry["type"]),
                        )

                    fetch_result = get_data_fetch()
                    select_result = unify_select_entry(
                        entry={"id": id}, db_name=db_name
                    )

                    debug = False

                    if debug:
                        print(fetch_result)
                        print(select_result)

                    if select_result is not None:
                        select_result = select_result[0]
                        flag_ignore_reader_count = True

                        def is_vital_version_same(
                            entry_a_timestamp: str, entry_b_timestamp: str
                        ) -> bool:
                            if entry_a_timestamp == entry_b_timestamp:
                                return True
                            else:
                                return False

                        def is_vital_content_same(
                            entry_a: dict, entry_b: dict, ignore_flag: bool
                        ) -> bool:
                            def remove_reader_count(src_dict) -> dict:
                                subdict_array_names = [
                                    "roles",
                                    "entryRelevances",
                                    "articleRelevances",
                                ]

                                def remove_in_subdict(subdict_array_name):
                                    working_subdict_array = src_dict.get(
                                        subdict_array_name
                                    )
                                    working_subdict_array_removed = []
                                    for subdict in working_subdict_array:
                                        if subdict.get("readerCount") != None:
                                            subdict.pop("readerCount")
                                        working_subdict_array_removed.append(
                                            subdict
                                        )
                                    return working_subdict_array_removed

                                for name in subdict_array_names:
                                    return_array = remove_in_subdict(name)
                                    src_dict.pop(name)
                                    src_dict[name] = return_array
                                return src_dict

                            if ignore_flag == True:
                                import copy

                                if remove_reader_count(
                                    copy.deepcopy(entry_a)
                                ) == remove_reader_count(
                                    copy.deepcopy(entry_b)
                                ):
                                    return True
                                else:
                                    return False
                            else:
                                if entry_a == entry_b:
                                    return True
                                else:
                                    return False

                        select_result.pop("_id")
                        if is_vital_content_same(
                            fetch_result,
                            select_result,
                            flag_ignore_reader_count,
                        ) and is_vital_version_same("", ""):
                            print("已有未过时的" + str(id) + "无需重复insert")
                            pass
                        else:
                            print("库内" + str(id) + "版本过时，需要insert")
                            update_entry(
                                pattern_entry={"id": id},
                                content_entry=fetch_result,
                                db_name=db_name,
                                collection_name="cngal."
                                + type2collection(fetch_result["type"]),
                            )  # 事实上应该update
                    else:
                        print("库内不存在" + str(id) + "条目，需要insert")
                        insert(fetch_result)

                maintain(id)
        # finish signal
        insert_entry(
            entry={
                "finish": True,
                "datetime": str(datetime.now()),
                "len": sum(
                    [
                        len(
                            select_entry(
                                pattern_entry={},
                                db_name=db_name,
                                collection_name="cngal." + type2collection(i),
                            )
                        )
                        for i in range(4)
                    ]
                ),
            },
            db_name=db_name,
            collection_name="cngal.config",
        )

    @print_time
    def build_graph():
        G = nx.DiGraph()
        count = 0
        count_limit = 500
        flag_count_limit_valid = False
        void_entities = []

        for code in type_code:
            collection_name = "cngal." + type2collection(code)
            collection = init_collection(
                client=init_connection(),
                db_name=db_name,
                collection_name=collection_name,
            )
            print("loaded: " + collection_name)
            for node in collection.find():
                G.add_node(str(node["id"]))

                # add edge

                # add edge function
                def add_edge(src, dst, *args, **kwargs):
                    if dst == "0":
                        void_entities.append([src, dst, kwargs])
                    else:
                        G.add_edge(src, dst)

                # productionGroups
                if "productionGroups" in node and isinstance(
                    node["productionGroups"], list
                ):
                    for group in node["productionGroups"]:
                        if isinstance(group, dict) and "id" in group:
                            target_id = str(group["id"])
                            add_edge(
                                str(node["id"]),
                                target_id,
                                key="productionGroups",
                                collection=collection_name,
                            )

                # publishers
                if "publishers" in node and isinstance(
                    node["publishers"], list
                ):
                    for group in node["publishers"]:
                        if isinstance(group, dict) and "id" in group:
                            target_id = str(group["id"])
                            add_edge(
                                str(node["id"]),
                                target_id,
                                key="publishers",
                                collection=collection_name,
                            )

                # roles
                if "roles" in node and isinstance(node["roles"], list):
                    for group in node["roles"]:
                        if isinstance(group, dict) and "id" in group:
                            target_id = str(group["id"])
                            add_edge(
                                str(node["id"]),
                                target_id,
                                key="roles",
                                collection=collection_name,
                            )

                # entryRelevances
                if "entryRelevances" in node and isinstance(
                    node["entryRelevances"], list
                ):
                    for group in node["entryRelevances"]:
                        if isinstance(group, dict) and "id" in group:
                            target_id = str(group["id"])
                            add_edge(
                                str(node["id"]),
                                target_id,
                                key="entryRelevances",
                                collection=collection_name,
                            )

                # staffs
                if "staffs" in node and isinstance(node["staffs"], list):
                    for staff in node["staffs"]:
                        if (
                            isinstance(staff, dict)
                            and "staffList" in staff
                            and isinstance(staff["staffList"], list)
                        ):
                            for item in staff["staffList"]:
                                if (
                                    isinstance(item, dict)
                                    and "names" in item
                                    and isinstance(item["names"], list)
                                ):
                                    for name in item["names"]:
                                        if (
                                            isinstance(name, dict)
                                            and "id" in name
                                        ):
                                            target_id = str(name["id"])
                                            add_edge(
                                                str(node["id"]),
                                                target_id,
                                                key="staffs",
                                                collection=collection_name,
                                            )

                # shutdown
                if (count + 1) % 500 == 0:
                    print("导入已进行到" + str(count + 1) + "个")
                count += 1
                if count >= count_limit and flag_count_limit_valid == True:
                    break

        # print(void_entities)
        return G

    finish_signal = bool(
        len(
            select_entry(
                pattern_entry={"finish": True},
                db_name=db_name,
                collection_name="cngal.config",
            )
        )
    )

    if not finish_signal:
        entry_meta_list = get_entry_meta_list()
        print("未检测到数据库完整标记，需要逐个条目检查是否已下载")
        get_entry_data(entry_meta_list, len(entry_meta_list) + 1)
    return build_graph()


# def vis_graph(G):
#     # 创建绘图对象
#     fig, ax = plt.subplots(figsize=(10, 10))
#
#     # 绘制有向图
#
#     def monkey_patching_timed_draw_networkx(*args, **kwargs):
#         time_start = time.time()
#         result = nx.draw_networkx(*args, **kwargs)  # 调用被替换的函数
#         time_end = time.time()
#         execution_time = time_end - time_start
#         message = "[TIME.{fn_name}]: {duration}s".replace(
#             "{fn_name}", "nx.draw_networkx"
#         ).replace("{duration}", str(round((execution_time), 3)))
#         print(message)
#         return result
#
#     # 替换原始函数并应用计时装饰器
#     nx_draw_networkx = nx.draw_networkx
#     nx_draw_networkx = monkey_patching_timed_draw_networkx
#
#     nx_draw_networkx(
#         G=G,
#         pos=nx.nx_pydot.graphviz_layout(G),
#         arrowsize=16,
#         node_size=800,
#         node_color="#8c564b",
#         with_labels=True,
#         font_size=14,
#         font_color="white",
#         alpha=0.9,
#         linewidths=0,
#         ax=ax,
#     )
#
#     ax.set_axis_off()
#     plt.show()


def vis_graph(G):
    import graphviz

    # 创建有向图对象
    dot = graphviz.Digraph(engine="twopi")

    # 添加节点和边
    for u, v in G.edges:
        dot.edge(str(u), str(v))

    # 设置节点属性
    for node in G.nodes:
        dot.node(
            str(node),
            shape="circle",
            style="filled,bold",
            color="#8c564b",
            fontcolor="white",
            fontsize="10",
            height="0.1",  # 调整节点高度
            width="0.1",  # 调整节点宽度
        )

    # 显示有向图
    dot.render(filename="../cngal.dot", directory=os.getcwd(), view=True)
    return dot


def detect_skipped_id(G):
    x = [int(i) for i in G.nodes()]
    x.sort()
    y = []
    for i in range(min(x), max(x) + 1):
        if i not in x:
            y.append(i)
    return len(x), len(y), min(x), max(x), y


def remove_isolated_nodes(G):
    isolated_nodes = list(nx.isolates(G))
    for node in isolated_nodes:
        G.remove_node(node)
    return G


def analyse_degree_frequency(G):
    graph_hist = nx.degree_histogram(G)
    in_degrees = nx.in_degree_centrality(G)
    out_degrees = nx.out_degree_centrality(G)
    for i in G.nodes():
        if in_degrees[i] + out_degrees[i] >= 0.8 * len(graph_hist):
            print(i)
    print(len(graph_hist))
    # print(graph_hist)

    # print(in_degrees)
    # print(out_degrees)


def beep():
    print("CnGal 中文GalGame资料站")  # from <title> of https://app.cngal.org/
