import os

import networkx as nx

from src.pycngal.const import type_code


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


def type2collection(type: int) -> str:
    return type_code[type]


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
