from http import HTTPStatus

from aiohttp import web
from helpers.login import is_authorized

from utils.database.note import insert_note, delete_note
from utils.logger import setup_logger

log = setup_logger(__name__)


async def note(request):
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    log.info("Notes preparation has started")
    user = request.user
    user_id = user.get("_id")

    if request.method == "POST":
        data = await request.json()
        log.info(data)
        text = data.get("text", "")
        file_id = data.get("file_id", "")
        await insert_note(owner_id=user_id, file_id=file_id, text=text)
        return web.json_response(status=HTTPStatus.CREATED)
    elif request.method == "DELETE":
        note_id = request.match_info.get('note_id')
        await delete_note(note_id=note_id)
        return web.json_response(status=HTTPStatus.NO_CONTENT)

    return web.json_response(status=HTTPStatus.METHOD_NOT_ALLOWED)
