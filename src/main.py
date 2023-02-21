from src.const import api_endpoint
from src.network import no_proxy, data_swagger_api

def init_graph():
    # get data
    data_swagger_api("/api/entries/GetAllEntriesIdName")
    # complete data
    data_swagger_api("/api/entries/GetEntryView/{id}")

def main():
    no_proxy(api_endpoint)



if __name__ == "__main__":
    main()
