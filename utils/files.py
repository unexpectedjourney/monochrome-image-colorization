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


async def handle_file_upload(request):
    reader = await request.multipart()
    field = await reader.next()
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
