from .connector import database

_users_collection = database.users


async def get_all_users():
    return await _users_collection.find()


async def get_user(_id=None, username=None):
    if _id is not None:
        return await _users_collection.find_one({"_id": _id})
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
