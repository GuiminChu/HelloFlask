from flask import Flask

from utils.factory import read_yaml
from utils.redis_util import Redis
from utils.exts import db, jwt, CustomJSONProvider
from utils.mqtt import mqtt
from utils.logger import logger
from utils.jobs import scheduler, Config

from api.user_api import bp_user
from api.auth_api import bp_auth
from api.device_model_api import bp_device_model
from api.device_switch_api import bp_device_switch
from api.task_api import bp_task
from api.test_api import bp_test

import config

app = Flask(__name__)
app.json = CustomJSONProvider(app)

app.config.from_object(config)
app.config.from_object(Config)

# db = SQLAlchemy(app)
db.init_app(app)
jwt.init_app(app)
# mqtt.init_app(app)

scheduler.init_app(app)
scheduler.start()

conf = read_yaml('resources/application.yml')
app.config.update(conf)

app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_device_model)
app.register_blueprint(bp_device_switch)
app.register_blueprint(bp_task)
app.register_blueprint(bp_test)


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
    app.run(host="0.0.0.0", port=8087)
    # app.run(debug=True)
