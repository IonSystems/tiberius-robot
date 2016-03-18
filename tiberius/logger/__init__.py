import logging


class Logger:

    def __init__(self):

        # Create logger for tiberius
        logger = logging.getLogger('tiberius')
        logger.setLevel(logging.DEBUG)

        # Create file handler for logger
        file_handler = logging.FileHandler('tiberius-log.log')
        file_handler.setLevel(logging.DEBUG)

        # Create console handler with higher logging level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create null handler for modules without another handler
        null_handler = logging.NullHandler()

        # Create a formatter for the log messages
        formatter = logging.Formatter(
            '%(asctime) - %(name) - %(levelname) - %(message)')

        # Adding handlers to logger

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.addHandler(null_handler)
