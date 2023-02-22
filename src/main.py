from src.const import api_endpoint
from src.network import no_proxy, request_swagger_api
from src.storage import init_collection, init_connection, insert_entry


def type2collection(type: int) -> str:
    if type == 0:
        return "game"
    if type == 1:
        return "character"
    if type == 2:
        return "maker"
    if type == 3:
        return "staff"


def init_graph():
    entry_meta_list = request_swagger_api(
        "/api/entries/GetAllEntriesIdName"
    )
    entry_list = {}

    def get_data():
        max_limit = len(entry_meta_list) + 1
        for entry_meta in entry_meta_list:
            id = entry_meta["id"]
            if id <= max_limit:
                entry = request_swagger_api(
                    "/api/entries/GetEntryView/{id}".replace("{id}", str(id))
                )
                post_id = insert_entry(
                    entry=entry,
                    collection=init_collection(
                        client=init_connection(),
                        db_name="cngal",
                        collection_name="cngal."
                        + type2collection(entry["type"]),
                    ),
                )
                entry_list[id] = post_id

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
    # init_graph()


if __name__ == "__main__":
    main()
