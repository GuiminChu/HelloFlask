from urllib.parse import quote_plus as urlquote
from datetime import timedelta

MYSQL_HOSTNAME = '223.99.197.190'
MYSQL_PORT = 13306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'Qn12345@'
MYSQL_DATABASE = 'qn_smart_home'
# 配置数据库的连接信息(因为密码里也有个@符号，所以先用 urlquote 编码一下)
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
# 关闭动态追踪修改的警告信息
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 展示sql语句
SQLALCHEMY_ECHO = True

MQTT_CLIENT_ID = "Consumer@12345_67890"
MQTT_BROKER_URL = '192.168.31.66'
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = 'MJKJ_OPEN'
MQTT_PASSWORD = 'MJKJ_OPEN'
MQTT_KEEPALIVE = 60
MQTT_TLS_ENABLED = False

JWT_SECRET_KEY = 'jwt-secret-string'
# 设置普通JWT过期时间
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
# 设置刷新JWT过期时间
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
