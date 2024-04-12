import logging
import os
from logging.handlers import RotatingFileHandler

from crypto_aggregator_telegram_bot.settings import BASE_DIR


def get_task_logger(task_name):
    logger = logging.getLogger(task_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_dir = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, f'{task_name}.log')

    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=100000, backupCount=1
    )
    file_handler.setFormatter(formatter)

    if len(logger.handlers) < 1:
        logger.addHandler(file_handler)
    return logger
