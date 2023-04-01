import json
import os
from pprint import pprint

import requests

from const import api_endpoint, headers


def no_proxy(domain: str) -> None:
    # If meet with this Error like this:
    # requests.exceptions.SSLError: HTTPSConnectionPool(host='https://domain', port=443): Max retries exceeded with url:
    # (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)')))
    os.environ["NO_PROXY"] = domain


def request_data_summary(tab="games"):
    if tab == "games":
        url = api_endpoint + "/api/tables/GetBasicInforList"
    elif tab == "group":
        url = api_endpoint + "/api/tables/GetGroupInforList"
    elif tab == "staff":
        url = api_endpoint + "/api/tables/GetStaffInforList"
    elif tab == "maker":
        url = api_endpoint + "/api/tables/GetMakerInforList"
    elif tab == "character":
        url = api_endpoint + "/api/tables/GetRoleInforList"
    elif tab == "price":
        url = api_endpoint + "/api/tables/GetSteamInforList"
    elif tab == "score":
        url = api_endpoint + "/api/tables/GetGameScoreList"
    else:
        print("数据汇总就这些分类没有其他的啦！写BUG了吧！")
    result_json = json.loads(requests.get(url=url, headers=headers).text)
    pprint(result_json)


def request_swagger_api(api_name: str) -> dict:
    return json.loads(
        requests.get(url=api_endpoint + api_name, headers=headers).text
    )


def beep():
    print("CnGal 中文GalGame资料站")  # from <title> of https://app.cngal.org/
