from aiohttp import web

from core.message_handler import rabbitmq_message_handler
from utils.constants import REQUEST_QUEUE
from utils.logger import setup_logger
from utils.rabbitmq.connector import RabbitMQConnection

log = setup_logger(__name__)
routes = web.RouteTableDef()


def main():
    log.info("Core application setup has started")
    app = web.Application()
    app.add_routes(routes)

    rabbitmq = RabbitMQConnection()
    rabbitmq.consume(REQUEST_QUEUE, rabbitmq_message_handler(rabbitmq))
    app['rabbitmq'] = rabbitmq

    web.run_app(app)
    log.info("Core application setup has finished")


if __name__ == '__main__':
    main()
