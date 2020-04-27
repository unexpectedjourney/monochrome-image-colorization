async def login(request):
    router = request.app.router
    form = await request.post()

    username, password = (form['name'], form['password'])

    pg = request.app.get('pg', None)
    if pg is not None:
        password = encrypt_password(password)
        user_id = await get_user_id(pg, username, password)
        if user_id is None:
            return web.Response(text='No such user', status=HTTPStatus.FORBIDDEN)
        user_id = dict(user_id)
        session = await new_session(request)
        session['user_id'] = user_id.get('id', None)
        return web.HTTPFound(router['index'].url_for())
    return web.Response(text='Server error', status=HTTPStatus.BAD_GATEWAY)