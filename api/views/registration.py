from http import HTTPStatus

from aiohttp import web

from helpers.encryption import encrypt_password, generate_token
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
    data = await request.json()
    username = data.get("username")
    password1 = data.get("password1")
    password2 = data.get("password2")
    if not username or not password1 or not password2:
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    if password1 != password2:
        return web.Response(
            text="Passwords should be similar", status=HTTPStatus.BAD_REQUEST)

    user_data = await user.get_user(username)
    if user_data is not None:
        return web.Response(
            text="User already exists", status=HTTPStatus.BAD_REQUEST)

    await user.insert_user_if_not_exist(username, encrypt_password(password1))
    user_data = await user.get_user(username)
    log.info(user_data)
    user_id = str(user_data.get('_id'))
    jwt_token = generate_token(user_id)
    return web.json_response({
        "token": jwt_token
    }, status=HTTPStatus.CREATED)
