import logging
import os
from datetime import datetime

LOG_FILE = "logs.txt"
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True
)
# custome_exceptionsifimported will invoke logger.INFo before logger.py can do it.since basicConfig can only be imported once, we need to add force=True in our basicConfig call
# . This was introduced in Python 3.8 and forces the basicConfig to override any existing handlers on the root logger.
# if __name__ == "__main__":
#     logging.info("Logger test message")