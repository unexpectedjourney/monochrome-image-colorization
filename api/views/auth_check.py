from http import HTTPStatus

from aiohttp import web

from helpers.login import is_authorized
from utils.logger import setup_logger

log = setup_logger(__name__)


async def check_authorization(request):
    """
        ---
        tags:
        - Authorization check
        responses:
            "200":
                description: user is authorized
            "405":
                description: invalid HTTP Method
    """
    log.info("Authorization check function has started")
    if await is_authorized(request):
        log.info("Authorization check has finished")
        return web.json_response(status=HTTPStatus.OK)
    log.info("Authorization check has finished")
    return web.json_response(status=HTTPStatus.UNAUTHORIZED)
