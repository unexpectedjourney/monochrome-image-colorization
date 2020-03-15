from utils.rabbitmq.message import RabbitMQMessage


async def _on_message(message, rabbitmq):
    message_obj = RabbitMQMessage.from_json(message)


def rabbitmq_message_handler(rabbitmq):
    async def wrapper(message):
        await _on_message(message, rabbitmq)
    return wrapper
