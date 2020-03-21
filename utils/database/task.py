from datetime import datetime

from motor import MotorClient


async def _tasks_collection():
    return (await MotorClient.get_database()).tasks


async def get_all_tasks():
    return (await _tasks_collection()).find()


async def get_one_task(task_id):
    return (await _tasks_collection()).find({"task_id": task_id})


async def insert_task(task_id):
    return (await _tasks_collection()).insert(
        {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "is_done": False
        }
    )


async def complete_task(task_id):
    return (await _tasks_collection()).update(
        {"task_id": task_id},
        {
            "$set": {
                "is_done": True
            }
        }
    )
