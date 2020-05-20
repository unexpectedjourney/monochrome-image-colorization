from datetime import datetime

from .connector import database

_files_collection = database.files


async def get_all_files():
    cursor = _files_collection.find()
    return [d async for d in cursor]


async def get_file(_id):
    return await _files_collection.find_one({"_id": _id})


async def get_files_by_owner_id(owner_id):
    cursor = _files_collection.find({"owner_id": owner_id})
    return [d async for d in cursor]


async def insert_file(owner_id):
    timestamp = datetime.now().isoformat()
    return await _files_collection.insert_one(
        {
            "created_at": timestamp,
            "update_at": timestamp,
            "owner_id": owner_id
        }
    )
