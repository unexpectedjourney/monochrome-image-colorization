from http import HTTPStatus

from aiohttp import web
from helpers.login import is_authorized

from utils.database.convertor import simplify_objects
from utils.database.history import get_history_records_by_owner_id
from utils.logger import setup_logger

log = setup_logger(__name__)


async def get_history_records(request):
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    log.info("History records preparation has started")
    user = request.user
    user_id = user.get("_id")
    history_records = await get_history_records_by_owner_id(owner_id=user_id)
    log.info(history_records)
    history_records = [
        simplify_objects(el, ('_id', 'owner_id')) for el in history_records
    ]
    log.info("History records preparation has finished")
    return web.json_response(history_records, status=HTTPStatus.OK)
