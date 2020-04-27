from .connector import client


async def _users_collection():
    return (await client.get_database()).users


async def get_all_users():
    return (await _users_collection()).find()


# todo add firstname and lastname
async def insert_user_if_not_exist(username, hashed_password):
    return (await _users_collection()).updateOne(
        {
            "username": username
        },
        {
            "$setOnInsert": {
                "username": username,
                "password": hashed_password}
        },
        {
            "upsert": True
        }
    )
