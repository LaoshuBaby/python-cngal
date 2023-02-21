from pprint import pprint

from src.const import api_endpoint
from src.network import no_proxy, request_swagger_api
from src.storage import init_connection


def init_graph():
    entry_id_list = request_swagger_api("/api/entries/GetAllEntriesIdName")
    pprint(entry_id_list)
    entry_list = []
    max_limit = 1
    for entry_meta in entry_id_list:
        id = entry_meta["id"]
        if id <= max_limit:
            entry = request_swagger_api(
                "/api/entries/GetEntryView/{id}".replace("{id}", str(id))
            )
            entry_list.append(entry)
    pprint(entry_list)


def main():
    # no_proxy(api_endpoint)
    # init_graph()
    init_connection()


if __name__ == "__main__":
    main()
