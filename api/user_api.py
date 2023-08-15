from flask import Blueprint, request
from model.entity.user_model import UserModel
from utils.exts import db
from api.rp import RP
import json

from utils.id_worker import idgen

bp_user = Blueprint('user', __name__, url_prefix='/user')


@bp_user.get('/info/<int:user_id>')
def user_info(user_id):
    user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        return RP.data(user)
    else:
        return RP.fail("用户不存在")


@bp_user.post('/save')
def save_user():
    data = json.loads(request.get_data(as_text=True))
    print(data)

    new_user = UserModel(**data)
    new_user.id = idgen.next_id()
    new_user.save()
    print(new_user.name)
    # new_user.name = "tom"
    # db.session.add(new_user)
    # db.session.commit()
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
