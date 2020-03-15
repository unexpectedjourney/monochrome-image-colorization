from aiohttp import web

from api.message_handler import rabbitmq_message_handler
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


def main():
    log.info("API application setup has started")
    app = web.Application()
    app.add_routes(routes)

    rabbitmq = RabbitMQConnection()
    rabbitmq.consume(RESPONSE_QUEUE, rabbitmq_message_handler(rabbitmq))
    app['rabbitmq'] = rabbitmq

    web.run_app(app)
    log.info("API application setup has finished")


if __name__ == '__main__':
    main()
