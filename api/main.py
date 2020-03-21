import asyncio
import uuid

from aiohttp import web

from message_handler import rabbitmq_message_handler
from utils.constants import RESPONSE_QUEUE, REQUEST_QUEUE
from utils.events import RabbitMQEvents
from utils.files import handle_file_upload
from utils.logger import setup_logger
from utils.rabbitmq.connector import RabbitMQConnection
from utils.rabbitmq.message import RabbitMQMessage

log = setup_logger(__name__)
routes = web.RouteTableDef()


@routes.get("/api/health")
async def status(request):
    return web.json_response({
        "status": "ok",
        "database": "ok",
        "api": "ok",
        "core": "ok"
    })


@routes.get("/api/colorize_file")
async def colorize(request):
    task_id = uuid.uuid4().hex
    rabbitmq = request.app['rabbitmq']

    filename = await handle_file_upload(request)

    message = RabbitMQMessage("api", RabbitMQEvents.REQUEST_COLORIZATION, {
        "filename": filename
    })
    rabbitmq.publish(queue=REQUEST_QUEUE, body=message.to_json())

    return web.json_response({
        "task_id": task_id
    })


async def main():
    log.info("API application setup has started")
    app = web.Application(client_max_size=2 ** 50)
    app.add_routes(routes)

    rabbitmq = RabbitMQConnection()
    await rabbitmq.connect()
    await rabbitmq.consume(RESPONSE_QUEUE, rabbitmq_message_handler(rabbitmq))
    app['rabbitmq'] = rabbitmq

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, port=8080)
    await site.start()

    log.info("API application setup has finished")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
