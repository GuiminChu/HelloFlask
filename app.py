from flask import Flask
from flask_jwt_extended import JWTManager

from utils.factory import read_yaml
from utils.redis_util import Redis
from utils.exts import db, CustomJSONProvider

from api.user_api import bp_user
from api.auth_api import bp_auth
from api.device_model_api import bp_device_model
from api.device_switch_api import bp_device_switch

from config import logger
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.json = CustomJSONProvider(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

# 配置数据库的连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True

# db = SQLAlchemy(app)
db.init_app(app)

conf = read_yaml('resources/application.yml')
app.config.update(conf)

app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_device_model)
app.register_blueprint(bp_device_switch)


# 测试一下连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text('select 1'))
#         print(rs.fetchone())


@app.route('/')
def hello_world():  # put application's code here
    logger.info('Hello, Flask!')
    return 'Hello, Flask!'


@app.route("/post/redis")
def test_redis():
    Redis.set('k', 'v')

    return 'true'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True)
