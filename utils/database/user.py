from bson.json_util import dumps
from bson.objectid import ObjectId

from .connector import database

_users_collection = database.users


async def get_all_users():
    cursor = _users_collection.find()
    return [d async for d in cursor]


async def get_user(_id=None, username=None):
    from utils.logger import setup_logger
    log = setup_logger(__name__)
    log.info(f"{_id}--{username}")
    if _id is not None:
        user =  await _users_collection.find_one({"_id": ObjectId(_id)})
        if user is not None:
            user["_id"] = str(user["_id"])
        return user
    else:
        return await _users_collection.find_one({"username": username})


# todo add firstname and lastname
async def insert_user_if_not_exist(username, hashed_password):
    return await _users_collection.update_one(
        {
            "username": username
        },
        {
            "$setOnInsert": {
                "username": username,
                "password": hashed_password
            }
        },
        upsert=True
    )
