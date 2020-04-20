from utils.logger import setup_logger

log = setup_logger(__name__)


async def colorize_file(params):
    log.info("Colorization has started")
    filename = params.get("filename")
    if not filename:
        return

    # part for image colorization
    # todo should pass new filename
    log.info("Colorization has finished")
    return filename
