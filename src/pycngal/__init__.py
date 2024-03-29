import json
import os
from typing import Optional

import requests

from .const import api_endpoint, headers


def request_swagger(format="json") -> Optional[dict]:
    if format == "json":
        return json.loads(
            requests.get(
                url="https://api.cngal.org/swagger/v1/swagger.json",
                headers=headers,
            ).text
        )
    elif format == "html":
        import webbrowser

        webbrowser.open("https://api.cngal.org/swagger/index.html")


def request_api(api_name: str) -> dict:
    return json.loads(
        requests.get(url=api_endpoint + api_name, headers=headers).text
    )


def request_data_summary(tab="games") -> Optional[dict]:
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
        return None
    return json.loads(requests.get(url=url, headers=headers).text)


def beep():
    print("CnGal 中文GalGame资料站")  # from <title> of https://app.cngal.org/
