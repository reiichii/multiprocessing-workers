import os
import uuid

from libs import logging
from libs.settings import TEMPLATE1_PATH, TEMPLATE2_PATH, TEST_CASE


def create_object(file_queue):
    logger = logging.getLogger()
    record = file_queue.get()
    path = f"../{TEST_CASE}/data/dummy_user_{record['user_id']}"
    filename = f"{record['item_id']}.json"
    file_path = f"{path}/{filename}"
    read_file = TEMPLATE1_PATH if record["default"] else TEMPLATE2_PATH

    os.makedirs(path, exist_ok=True)

    with open(read_file) as f:
        template = f.read()

    with open(file_path, mode="w") as f:
        f.write(template.replace("{{params}}", str(uuid.uuid4())))

    logger.info(f"created: {file_path}")
