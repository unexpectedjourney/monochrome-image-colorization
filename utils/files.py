import os
import uuid

from PIL import Image

from utils.constants import UPLOAD_PATH
from utils.logger import setup_logger

log = setup_logger(__name__)


def trim_filename(filename):
    if filename:
        return filename.encode(errors='replace')[-100:].decode(
            errors='replace')
    return filename


def generate_filename(filename):
    return os.path.join(
        UPLOAD_PATH,
        '{}.{}'.format(str(uuid.uuid4()), trim_filename(filename))
    )


async def save_file(field):
    log.info(field.filename)
    pure_filename = field.filename
    filename = generate_filename(pure_filename)

    log.debug('Trying to write file')
    size = 0
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    return filename, pure_filename


def crop_image(filepath, left, top, right, bottom):
    im = Image.open(filepath)
    im = im.convert('RGB')
    im = im.crop((left, top, right, bottom))
    im.save(filepath)


async def handle_file_upload(request):
    (
        original_filename, painted_filename, pure_filename, image_title
    ) = None, None, None, None
    left, top, right, bottom = (0, 0, 0, 0)
    async for field in (await request.multipart()):
        if field.name == "originalImage":
            original_filename, pure_filename = await save_file(field)
        elif field.name == "paintedImage":
            painted_filename, pure_filename = await save_file(field)
        elif field.name == "projectTitle":
            image_title = (await field.read()).decode("utf-8")
        elif field.name == "top":
            top = int(float((await field.read()).decode("utf-8")))
        elif field.name == "bottom":
            bottom = int(float((await field.read()).decode("utf-8")))
        elif field.name == "left":
            left = int(float((await field.read()).decode("utf-8")))
        elif field.name == "right":
            right = int(float((await field.read()).decode("utf-8")))
    for path_data in (original_filename, painted_filename):
        crop_image(path_data, left, top, right, bottom)
    return original_filename, painted_filename, pure_filename, image_title
