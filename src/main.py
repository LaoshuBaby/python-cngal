from pprint import pprint

from src.const import api_endpoint
from src.network import no_proxy, request_swagger_api
from src.storage import init_connection, init_collection, insert_entry


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
    entry_meta_list = request_swagger_api("/api/entries/GetAllEntriesIdName")
    max_limit = len(entry_meta_list) + 1
    entry_list = {}
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
                    collection_name="cngal." + type2collection(entry["type"]),
                ),
            )
            entry_list[id] = post_id

    print(entry_list)


def main():
    no_proxy(api_endpoint)
    init_graph()


if __name__ == "__main__":
    main()
