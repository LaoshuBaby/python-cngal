from typing import List, Optional

from pymongo import MongoClient

from const import type_code


def init_connection():
    client = MongoClient("mongodb://localhost:27017/")
    return client


def init_collection(
    client=None, db_name=None, collection_name=None
) -> Optional[MongoClient]:
    if db_name != None and collection_name != None:
        db = client[db_name]
        collection = db[collection_name]
        return collection
    else:
        return None


def insert_entry(
    entry: dict, collection=None, db_name=None, collection_name=None
) -> Optional[str]:
    if db_name != None and collection_name != None:
        collection = init_collection(
            client=init_connection(),
            db_name=db_name,
            collection_name=collection_name,
        )
    if collection != None:
        post_id = collection.insert_one(entry).inserted_id
        return post_id
    else:
        return None


def select_entry(
    pattern_entry: dict, collection=None, db_name=None, collection_name=None
) -> Optional[list]:
    if db_name != None and collection_name != None:
        collection = init_collection(
            client=init_connection(),
            db_name=db_name,
            collection_name=collection_name,
        )
    if collection != None:
        get = collection.find(pattern_entry)
        result = [document for document in get]
        return result
    else:
        return None


def update_entry(
    pattern_entry: dict,
    content_entry: dict,
    collection=None,
    db_name=None,
    collection_name=None,
) -> None:
    if db_name != None and collection_name != None:
        collection = init_collection(
            client=init_connection(),
            db_name=db_name,
            collection_name=collection_name,
        )
    if collection != None:
        collection.replace_one(pattern_entry, content_entry)
    else:
        print("更新不成功")


def unify_select_entry(entry: dict, db_name: str) -> Optional[List[dict]]:
    for code in type_code:
        result = select_entry(
            pattern_entry=entry,
            db_name=db_name,
            collection_name="cngal." + type_code[code],
        )
        if result != []:
            return result
    return None
