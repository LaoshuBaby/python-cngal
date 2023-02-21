import json
import os
from pprint import pprint

import requests

api_endpoint = "https://api.cngal.org/api/"
headers={
    "User-Agent":"python-cngal /technical-preview"
}


def no_proxy(domain: str) -> None:
    # If meet with this Error like this:
    # requests.exceptions.SSLError: HTTPSConnectionPool(host='https://domain', port=443): Max retries exceeded with url:
    # (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)')))
    os.environ["NO_PROXY"] = domain


def data_summary(tab="games"):
    if tab == "games":
        url = api_endpoint + "tables/GetBasicInforList"
    elif tab == "group":
        url = api_endpoint + "tables/GetGroupInforList"
    elif tab == "staff":
        url = api_endpoint + "tables/GetStaffInforList"
    elif tab == "maker":
        url = api_endpoint + "tables/GetMakerInforList"
    elif tab == "character":
        url = api_endpoint + "tables/GetRoleInforList"
    elif tab == "price":
        url = api_endpoint + "tables/GetSteamInforList"
    elif tab == "score":
        url = api_endpoint + "tables/GetGameScoreList"
    else:
        print("数据汇总就这些分类没有其他的啦！写BUG了吧！")
    result_json=json.loads(requests.get(url=url,headers=headers).text)
    pprint(result_json)


def main():
    no_proxy(api_endpoint)
    data_summary("maker")


if __name__ == "__main__":
    main()
