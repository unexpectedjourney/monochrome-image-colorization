from aiohttp import web
from views.auth_check import check_authorization
from views.files import (colorize, save_file_version, get_user_files)
from views.health import status
from views.login import login
from views.registration import register


def get_urls():
    return [
        web.get("/api/health/", status, name="status"),
        web.post("/api/colorize_file/", colorize, name="colorize"),
        web.post("/api/save_file/", save_file_version, name="save_file"),
        web.get("/api/images/", get_user_files, name="images"),
        web.get("/api/check_authorization/", check_authorization,
                name="check_authorization"),
        web.post("/login/", login, name="login"),
        web.post("/register/", register, name="register"),
    ]


def get_routers(app):
    routers = []
    routers.extend(get_urls())
    app.add_routes(routers)
