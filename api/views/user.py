from http import HTTPStatus

from aiohttp import web
from helpers.login import is_authorized

from utils.database.convertor import simplify_objects
from utils.database.user import update_user, get_user
from utils.logger import setup_logger

log = setup_logger(__name__)


async def user_info(request):
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    log.info("User profile preparation has started")
    user = request.user

    if request.method == "PUT":
        user_id = request.match_info.get('user_id')
        original_user_id = user.get("_id")
        username = user.get("username")
        if user_id != original_user_id:
            return web.json_response(status=HTTPStatus.FORBIDDEN)

        data = await request.json()
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email")

        await update_user(
            username=username, first_name=first_name, last_name=last_name,
            email=email)
        user = await get_user(username=username)
        user = simplify_objects(user)
        log.info(user)
    log.info("User profile preparation has finished")
    return web.json_response(user, status=HTTPStatus.OK)
