import jwt
from aiohttp.web_response import json_response
from helpers.encryption import JWT_SECRET, JWT_ALGORITHM

from utils.database import user


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except jwt.DecodeError:
                return json_response(
                    {'message': 'Token is invalid'}, status=400)

            user_id = payload.get('user_id', None)
            if user_id is not None:
                request.user = await user.get_user(_id=user_id)
        return await handler(request)

    return middleware
