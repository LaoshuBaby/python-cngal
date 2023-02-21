from datetime import datetime
from typing import Optional

from pymongo import MongoClient


def init_connection():
    client = MongoClient("mongodb://localhost:27017/")
    return client


def init_collection(client=None, db_name=None, collection_name=None):
    if db_name == None and collection_name == None:
        db = client["cngal"]
        collection = db["cngal.logs"]
        post_id = collection.insert_one(
            {"time": str(datetime.now())}
        ).inserted_id
    else:
        db = client[db_name]
        collection = db[collection_name]
        return collection


def insert_entry(entry: dict, collection=None) -> Optional[str]:
    post_id = collection.insert_one(entry).inserted_id
    return post_id


# def debug():
#     db.list_collection_names()


def insert():
    pass
