from datetime import datetime

from src.const import api_endpoint, db_name
from src.network import no_proxy, request_swagger_api
from src.database import init_collection, init_connection, insert_entry, select_entry

type_code={
    0:"game",
    1:"character",
    2:"maker",
    3:"staff"
}


def type2collection(type: int) -> str:
    return type_code[type]


def init_graph():
    entry_meta_list = request_swagger_api("/api/entries/GetAllEntriesIdName")
    entry_list = {}

    def get_data():
        max_limit = 20#len(entry_meta_list) + 1
        for entry_meta in entry_meta_list:
            id = entry_meta["id"]
            if id <= max_limit:
                # get
                entry = request_swagger_api(
                    "/api/entries/GetEntryView/{id}".replace("{id}", str(id))
                )
                # select and judge
                def unify_select_entry(entry:dict,db_name:str):
                    for code in type_code:
                        print(type_code[code], entry)
                        result=select_entry(entry=entry, db_name=db_name, collection_name="cngal."+type_code[code])
                        print(str(result))
                        if result!=None:
                            return result
                if result:=unify_select_entry(entry={"id": id},db_name=db_name)!=None:
                    # judge whether the same data
                    # if same, skip insert
                    pass
                else:
                    # insert
                    post_id = insert_entry(
                        entry=entry,
                        db_name=db_name,
                        collection_name="cngal." + type2collection(entry["type"]),
                    )
                    entry_list[id] = str(post_id)
                    print("id: " + str(id), "post_id: " + str(post_id))
        insert_entry(entry={"finish": True, "datetime": str(datetime.now())},db_name=db_name,collection_name="cngal.config")

    def build_graph():
        # game-maker
        # game-staff
        # game-character
        import networkx as nx

        G = nx.Graph()
        for i in range(len(entry_meta_list)):
            G.add_node(entry_meta_list[i]["id"])
            # append entry_list[id] (contain name)
        pass

    # if cngal.config haven't got a is_finish==True, that we need to get_data
    # do we need to select and compare before insert? if have different? delete old one or drop memory one?
    get_data()
    build_graph()


def main():
    no_proxy(api_endpoint)
    init_graph()


if __name__ == "__main__":
    main()
