from http import HTTPStatus

from aiohttp import web
from helpers.encryption import encrypt_password, generate_token

from utils.database import user
from utils.database.history import insert_history_record
from utils.history_types import HistoryTypes


async def login(request):
    """
    ---
    tags:
    - Login
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
          password:
            type: string
    responses:
        "200":
            description: registered
        "400":
            description: wrong data
        "405":
            description: invalid HTTP Method
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    hashed_password = encrypt_password(password)
    user_data = await user.get_user(username=username)
    if user_data is None:
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    original_hashed_password = user_data.get("password")

    if original_hashed_password != hashed_password:
        return web.Response(
            text="Wrong password", status=HTTPStatus.BAD_REQUEST)

    user_id = str(user_data.get("_id"))
    jwt_token = generate_token(user_id)
    await insert_history_record(user_id, HistoryTypes.USER_LOGGED_IN.value)

    return web.json_response({
        "token": jwt_token
    }, status=HTTPStatus.ACCEPTED)
