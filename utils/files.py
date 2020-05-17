import os
import uuid

from utils.constants import UPLOAD_PATH
from utils.logger import setup_logger

log = setup_logger(__name__)


def trim_filename(filename):
    if filename:
        return filename.encode(errors='replace')[-100:].decode(
            errors='replace')
    return filename


async def save_file(field):
    log.info(field.filename)
    filename = os.path.join(
        UPLOAD_PATH,
        '{}.{}'.format(str(uuid.uuid4()), trim_filename(field.filename)))

    log.debug('Trying to write file')
    size = 0
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    return filename


async def handle_file_upload(request):
    original_filename, painted_filename = None, None
    async for field in (await request.multipart()):
        if field.name == "originalImage":
            original_filename = await save_file(field)
        elif field.name == "paintedImage":
            painted_filename = await save_file(field)

    return original_filename, painted_filename
