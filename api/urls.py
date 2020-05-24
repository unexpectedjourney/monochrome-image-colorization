from aiohttp import web
from views.auth_check import check_authorization
from views.files import (
    colorize, save_file_version, get_user_files, get_user_file,
    get_file_versions)
from views.health import status
from views.login import login
from views.registration import register
from views.notes import note
from views.user import user_info


def get_urls():
    return [
        web.get("/api/health/", status, name="status"),

        web.get("/api/images/", get_user_files, name="get_images"),
        web.get("/api/images/{image_id}", get_user_file, name="get_image"),
        web.get("/api/images/{image_id}/versions", get_file_versions,
                name="get_image_versions"),
        web.post("/api/colorize_file/", colorize, name="colorize"),
        web.post("/api/save_file/", save_file_version, name="save_file"),

        web.post("/api/note/", note, name="add_note"),
        web.delete("/api/note/{note_id}", note, name="delete_note"),

        web.get("/api/check_authorization/", check_authorization,
                name="check_authorization"),
        web.post("/login/", login, name="login"),
        web.post("/register/", register, name="register"),

        web.get("/api/users/", user_info, name="get_user"),
        web.put("/api/users/{user_id}", user_info, name="put_user"),
    ]


def get_routers(app):
    routers = []
    routers.extend(get_urls())
    app.add_routes(routers)
