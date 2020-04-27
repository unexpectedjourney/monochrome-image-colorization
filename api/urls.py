from aiohttp import web

from views.colorization import colorize
from views.health import status
from views.login import login
from views.registration import register


def get_urls():
    return [
        web.get("/api/health/", status, name="status"),
        web.post("/api/colorize_file/", colorize, name="colorize"),
        web.post("/login/", login, name="login"),
        web.post("/register/", register, name="register"),
    ]


def get_routers(app):
    routers = []
    routers.extend(get_urls())
    app.add_routes(routers)
