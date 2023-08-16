import os
import sys
from loguru import logger

log_level = os.environ.get('log_level', 'INFO')

logger.remove()
logger.add(sys.stdout, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>',
           level=log_level)
