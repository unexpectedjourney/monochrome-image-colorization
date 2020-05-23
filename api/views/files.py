import uuid
from http import HTTPStatus

from aiohttp import web
from bson import ObjectId
from helpers.login import is_authorized

from utils.constants import REQUEST_QUEUE
from utils.database.convertor import simplify_objects
from utils.database.file import insert_file, get_files_by_owner_id, get_file
from utils.database.file_version import insert_file_version, \
    get_file_versions_by_file_id
from utils.database.note import get_notes_by_file_id
from utils.events import RabbitMQEvents
from utils.files import handle_file_upload, save_file
from utils.logger import setup_logger
from utils.rabbitmq.message import RabbitMQMessage

log = setup_logger(__name__)


async def colorize(request):
    """
    ---
    tags:
    - Colorization
    produces:
    - multipart/form-data
    parameters:
    - in: formData
      name: originalImage
      type: file
      required: true
    - in: formData
      name: paintedImage
      type: file
      required: true
    - in: formData
      name: projectTitle
      type: string
      required: false
    responses:
      "201":
        description: task was created
      "400":
        description: wrong data
      "405":
        description: invalid HTTP Method
    """
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)

    log.info("Colorization function has started")
    task_id = uuid.uuid4().hex
    rabbitmq = request.app['rabbitmq']

    (
        original_filename, painted_filename, pure_filename, image_title
    ) = await handle_file_upload(request)

    user = request.user
    log.info(user)
    user_id = user.get("_id")
    file_result = await insert_file(owner_id=user_id, title=image_title)
    file_id = file_result.inserted_id
    await insert_file_version(filepath=original_filename, file_id=file_id)
    await insert_file_version(filepath=painted_filename, file_id=file_id)

    message = RabbitMQMessage(
        "api", RabbitMQEvents.REQUEST_COLORIZATION.value, {
            "original_filename": original_filename,
            "painted_filename": painted_filename,
            "pure_filename": pure_filename,
            "file_id": file_id
        }
    )
    await rabbitmq.publish(queue=REQUEST_QUEUE, body=message.to_json())

    log.info("Colorization function has finished")
    return web.json_response({
        "task_id": task_id
    }, status=HTTPStatus.CREATED)


async def save_file_version(request):
    """
    ---
    tags:
    - File save
    produces:
    - multipart/form-data
    parameters:
    - in: formData
      name: file
      type: file
      required: true
    - in: formData
      name: file_id
      type: string
      required: true
    responses:
      "201":
        description: file_version is saved
      "400":
        description: wrong data
      "405":
        description: invalid HTTP Method
    """
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    filepath, file_id = None, None
    async for field in (await request.multipart()):
        if field.name == "file":
            filepath, pure_filename = await save_file(field)
        elif field.name == "file_id":
            file_id = (await field.read()).decode("utf-8")
    await insert_file_version(filepath=filepath, file_id=file_id)
    return web.json_response(status=HTTPStatus.CREATED)


async def get_user_files(request):
    """
        ---
        tags:
        - Files get
        responses:
          "200":
            description: Files were taken
          "405":
            description: invalid HTTP Method
    """
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    log.info("Files preparation has started")
    user = request.user
    user_id = user.get("_id")
    files = await get_files_by_owner_id(user_id)
    for file in files:
        file_id = file.get("_id")
        file["_id"] = str(file_id)
        file_versions = await get_file_versions_by_file_id(file_id=file_id)
        if not file_versions:
            continue
        file_version = file_versions[0]
        file["filepath"] = file_version.get("filepath")
    log.info("Files preparation has finished")
    return web.json_response(files, status=HTTPStatus.OK)


async def get_user_file(request):
    """
        ---
        tags:
        - File get
        responses:
          "200":
            description: Files were taken
          "405":
            description: invalid HTTP Method
    """
    if not await is_authorized(request):
        log.info("Authorization has failed")
        return web.json_response(status=HTTPStatus.UNAUTHORIZED)
    log.info("One file preparation has started")

    file_id = request.match_info.get('image_id')
    file = await get_file(file_id)
    if file is None:
        return web.json_response(status=HTTPStatus.NOT_FOUND)
    user = request.user
    user_id = user.get("_id")
    file_owner_id = file.get("owner_id")
    if user_id != file_owner_id:
        return web.json_response(status=HTTPStatus.Forbidden)

    file["_id"] = file_id
    file_versions = await get_file_versions_by_file_id(file_id=ObjectId(file_id))

    if file_versions:
        file_version = file_versions[0]
        file["filepath"] = file_version.get("filepath")

    notes = await get_notes_by_file_id(file_id)
    file["notes"] = [simplify_objects(el) for el in notes]
    log.info(file)
    log.info("One file preparation has finished")
    return web.json_response(file, status=HTTPStatus.OK)
