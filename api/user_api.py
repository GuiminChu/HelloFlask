# https://www.bilibili.com/read/cv24640972
# Flask-SQLAlchemy 3.0 版本 基本操作
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/

from flask import Blueprint, request
from model.entity.user_model import UserModel
from utils.exts import db
from model.rp import RP
import json

from utils.id_worker import idgen
from utils.digest_util import DigestUtil

bp_user = Blueprint('user', __name__, url_prefix='/user')


@bp_user.get('/page')
def user_page():
    page = request.args.get('current', 1, type=int)
    per_page = request.args.get('size', 10, type=int)

    select = db.select(UserModel).order_by(UserModel.create_time.desc())
    page = db.paginate(select, page=page, per_page=per_page)

    result = {
        'records': [user for user in page.items],
        "total": page.total,  # 总记录数
        "size": page.per_page,  # 每页显示的记录数
        "current": page.page,  # 当前页数
        "pages": page.pages  # 总页数
    }

    return RP.data(result)
    # return RP.data([user for user in users])


@bp_user.get('/list')
def user_list():
    users = db.session.execute(db.select(UserModel).order_by(UserModel.create_time.desc())).scalars()
    print(type(users))
    return RP.data([user for user in users])


@bp_user.get('/info/<int:user_id>')
def user_info(user_id):
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        return RP.data(user)
    else:
        return RP.fail("用户不存在")


@bp_user.post('/save')
def save_user():
    username = request.json.get("username", None)
    if username is None or not isinstance(username, str):
        return RP.fail("请输入正确的用户名")
    if len(username) < 4 or len(username) > 20:
        return RP.fail("用户名称长度不正确")

    select = db.select(UserModel).where(UserModel.is_deleted == 0).where(UserModel.account == username)
    users = db.session.execute(select).all()

    if len(users) > 0:
        return RP.fail('用户名重复')

    request_body = json.loads(request.get_data(as_text=True))
    print(request_body)

    new_user = UserModel.from_dict(request_body)

    new_user.id = idgen.next_id()

    new_user.account = username
    # 对密码进行加密
    new_user.password = DigestUtil.sha256(request_body.get('password', '123456'))
    new_user.save()
    print(new_user.name)
    return RP.data(new_user)


@bp_user.post('/update')
def update_user():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    user_id = data.get('id')
    if not user_id:
        return RP.fail('id不能为空')

    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    user.name = data.get('name')
    db.session.commit()
    return RP.data(user)
