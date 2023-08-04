from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from markupsafe import escape
from urllib.parse import quote_plus as urlquote

from sqlalchemy import text

from api.rp import RP

app = Flask(__name__)

HOSTNAME = '192.168.1.252'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'Qn12345@'
DATABASE = 'demo'
# 因为密码里也有个@符号，所以先用 urlquote 编码一下
CONN_INFO = f'mysql+pymysql://{USERNAME}:{urlquote(PASSWORD)}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

# 配置数据库的连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = CONN_INFO
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class User(db.Model):
    # 指定模型类对应的数据库表名。如果不指定，则默认为类名的小写形式。
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True)
    mobile = db.Column(db.String(20), doc='手机号')
    password = db.Column(db.String(80), doc='密码')
    email = db.Column(db.String(120), doc='邮箱')
    is_delete = db.Column(db.Boolean, default=False, doc='是否删除')


# 测试一下连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text('select 1'))
#         print(rs.fetchone())


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello, Flask!'


@app.route('/json', methods=['GET'])
def get_json():
    data = {
        "name": "python",
        "age": 18
    }
    # return jsonify(data)
    return jsonify(RP.status(True))


@app.route("/user/<username>")
def show_user_profile(username):
    return f'User {escape(username)}'


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f'Post {post_id}'


@app.route("/path/<path:subpath>")
def show_path(subpath):
    return f'Path {escape(subpath)}'
    # http://127.0.0.1:5000/path/%3Cscript%3Ealert(%22bad%22)%3C/script%3E
    # return f'Path {subpath}'


if __name__ == '__main__':
    app.run(debug=True)
