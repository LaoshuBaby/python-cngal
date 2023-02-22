from typing import Optional

from pymongo import MongoClient


def init_connection():
    client = MongoClient("mongodb://localhost:27017/")
    return client


def init_collection(client=None, db_name=None, collection_name=None)->Optional[MongoClient]:
    if db_name == None or collection_name == None:
        return None
    else:
        db = client[db_name]
        collection = db[collection_name]
        return collection


def insert_entry(entry: dict, collection=None, db_name=None, collection_name=None) -> Optional[str]:
    if db_name!= None and collection_name!=None:
        collection = init_collection(
            client=init_connection(),
            db_name=db_name,
            collection_name=collection_name
        )
    if collection!=None:

        post_id = collection.insert_one(entry).inserted_id
        return post_id
    else:
        return None


# def debug():
#     db.list_collection_names()


def insert():
    pass
