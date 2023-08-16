import os
import sys
from loguru import logger
from urllib.parse import quote_plus as urlquote

log_level = os.environ.get('log_level', 'INFO')

logger.remove()
logger.add(sys.stdout, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>',
           level=log_level)

MYSQL_HOSTNAME = '223.99.197.190'
MYSQL_PORT = 13306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'Qn12345@'
MYSQL_DATABASE = 'qn_smart_home'
# 因为密码里也有个@符号，所以先用 urlquote 编码一下
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
