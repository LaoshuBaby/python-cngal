# init 4 table in mongodb, "games", "staff", "article", "character"

# How to judge? by "type":0/1/2/3 ?

# according to my guess
# 0 game
# 1 character
# 2 maker
# 3 staff


from pymongo import MongoClient


def init_mongo():
    # only when there never a database and never a table
    pass


def init_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client["cngal"]
    collection = db["cngal.games"]
    post = {
        "author": "CNGAL",
        "text": "My first VN!",
        "tags": ["mongodb", "python", "pymongo"],
    }
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    db.list_collection_names()
    # if collection name won't valid, call init


def insert():
    pass
