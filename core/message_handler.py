from colorization import colorize_file
from utils.constants import RESPONSE_QUEUE
from utils.events import RabbitMQEvents
from utils.logger import setup_logger
from utils.rabbitmq.message import RabbitMQMessage

log = setup_logger(__name__)


async def _on_message(message, rabbitmq):
    message_obj = RabbitMQMessage.from_json(message)

    message_type = message_obj.message_type
    message_params = message_obj.message_params

    if not message_type or not message_params:
        return

    if message_type == RabbitMQEvents.REQUEST_COLORIZATION:
        filename = await colorize_file(message_params)
        if filename:
            message = RabbitMQMessage(
                "core", RabbitMQEvents.RESPONSE_COLORIZATION, {
                    "filename": filename
                })
            rabbitmq.publish(queue=RESPONSE_QUEUE, body=message.to_json())
    else:
        log.warn("Unknown message_type was found")


def rabbitmq_message_handler(rabbitmq):
    async def wrapper(message):
        await _on_message(message, rabbitmq)

    return wrapper
