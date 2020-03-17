import asyncio

from aiohttp import web

from message_handler import rabbitmq_message_handler
from utils.constants import RESPONSE_QUEUE
from utils.logger import setup_logger
from utils.rabbitmq.connector import RabbitMQConnection

log = setup_logger(__name__)
routes = web.RouteTableDef()


@routes.get("/api/status")
async def status(request):
    return web.json_response({
        "status": "ok"
    })


async def main():
    log.info("API application setup has started")
    app = web.Application()
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
