from flask import Flask, jsonify

from urllib.parse import quote_plus as urlquote

from utils.factory import read_yaml
from utils.redis_util import Redis
from utils.exts import db, CustomJSONProvider

from api.user_api import bp_user

app = Flask(__name__)
app.json = CustomJSONProvider(app)

HOSTNAME = '192.168.1.252'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'Qn12345@'
DATABASE = 'qn_smart_home'
# 因为密码里也有个@符号，所以先用 urlquote 编码一下
CONN_INFO = f'mysql+pymysql://{USERNAME}:{urlquote(PASSWORD)}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

# 配置数据库的连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = CONN_INFO
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True

# db = SQLAlchemy(app)
db.init_app(app)

conf = read_yaml('resources/application.yml')
app.config.update(conf)

app.register_blueprint(bp_user)


# 测试一下连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text('select 1'))
#         print(rs.fetchone())


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello, Flask!'


@app.route("/post/redis")
def test_redis():
    Redis.set('k', 'v')
    return 'true'


if __name__ == '__main__':
    app.run(debug=True)
