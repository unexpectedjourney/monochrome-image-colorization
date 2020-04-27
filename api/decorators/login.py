from http import HTTPStatus

from aiohttp import web
from aiohttp_session import get_session


async def update_session(request, session):
    if request is not None and request.user is not None:
        session['user_id'] = request.user.get('_id', None)


def is_authorized(function):
    async def wrapped(request, *args, **kwargs):
        session = await get_session(request)
        await update_session(request, session)
        if 'user_id' not in session or session['user_id'] is None:
            return web.json_response(status=HTTPStatus.UNAUTHORIZED)
        return await function(request, *args, **kwargs)

    return wrapped
