# init 4 table in mongodb, "games", "staff", "article", "character"

# How to judge? by "type":0/1/2/3 ?

# according to my guess
# 0 game
# 1 character
# 2 maker
# 3 staff


from pymongo import MongoClient
from datetime import datetime


def init_connection():
    client = MongoClient("mongodb://localhost:27017/")
    return client


def init_collection(client=None, db_name=None, collection_name=None):
    if db_name == None and collection_name == None:
        db = client["cngal"]
        collection = db["cngal.logs"]
        post_id = collection.insert_one({"time": str(datetime.now())}).inserted_id
    else:
        db = client[db_name]
        collection = db[collection_name]
        return collection


def insert_entry(entry: dict, collection=None):
    if entry["type"] == 0:
        post_id = collection.insert_one(entry).inserted_id
        print(post_id)

# def debug():
#     db.list_collection_names()


def insert():
    pass
