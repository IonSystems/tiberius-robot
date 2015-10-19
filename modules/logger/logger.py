import logging


#Create logger for tiberius
logger = logging.getLogger('tiberius')
logger.setLevel(logging.DEBUG)

#Create file handler for logger
file_handler = logging.FileHandler('tiberius-log.log')
file_handler.setLevel(logging.DEBUG)

#Create console handler with higher logging level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

#Create null handler for modules without another handler
null_handler = logging.NullHandler()

#Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
#Adding handlers to logger

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(null_handler)

logger.info("Logging Configured")
