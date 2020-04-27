import uuid
from http import HTTPStatus

from aiohttp import web

from utils.constants import REQUEST_QUEUE
from utils.events import RabbitMQEvents
from utils.files import handle_file_upload
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
          name: file1
          type: file
          required: true
        - in: formData
          name: file2
          type: file
          required: true
        responses:
            "201":
                description: task was created
            "400":
                description: wrong data
            "405":
                description: invalid HTTP Method
    """
    log.info("Colorization function has started")
    task_id = uuid.uuid4().hex
    rabbitmq = request.app['rabbitmq']

    filename = await handle_file_upload(request)

    message = RabbitMQMessage(
        "api", RabbitMQEvents.REQUEST_COLORIZATION.value, {
            "filename": filename
        }
    )
    await rabbitmq.publish(queue=REQUEST_QUEUE, body=message.to_json())

    log.info("Colorization function has finished")
    return web.json_response({
        "task_id": task_id
    }, status=HTTPStatus.CREATED)
