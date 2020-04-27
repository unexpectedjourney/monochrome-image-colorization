from http import HTTPStatus

from aiohttp import web

from helpers.encryption import encrypt_password
from utils.database import user
from utils.logger import setup_logger

log = setup_logger(__name__)


async def register(request):
    """
        ---
        tags:
        - Register
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Created user object
          required: true
          schema:
            type: object
            properties:
              username:
                type: "string"
              firstName:
                type: string
              lastName:
                type: string
              password1:
                type: string
              password2:
                type: string
        responses:
            "201":
                description: registered
            "400":
                description: wrong data
            "405":
                description: invalid HTTP Method
    """
    data = await request.post()

    username = data.get("username")
    password1 = data.get("password1")
    password2 = data.get("password2")

    if not username or not password1 or not password2:
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    if password1 != password2:
        return web.Response(
            text="Passwords should be similar", status=HTTPStatus.BAD_REQUEST)

    data = user.insert_user_if_not_exist(username, encrypt_password(password1))
    log.info(data)
    return web.json_response(status=HTTPStatus.CREATED)
