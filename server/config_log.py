import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('error.log')
formatter = logging.Formatter('%(asctime)s:%(filename)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)