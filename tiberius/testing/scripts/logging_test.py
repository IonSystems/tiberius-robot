import sys
from tiberius.logger import logger
import logging
d_logger = logging.getLogger('tiberius.testing')
import time
if __name__ == "__main__":
    while True:
        time.sleep(1)
        d_logger.info("Hello")
        d_logger.error("Test error")
        d_logger.warn("Test warning")
        d_logger.critical("Test critical")
