import logging
import datetime

#create test logger
today = datetime.datetime.now().strftime('%Y%m%d')
logger = logging.getLogger('dwetl')
file_handler = logging.FileHandler(f'logs/test.dwetl.log.{today}')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)