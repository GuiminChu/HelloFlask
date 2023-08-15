from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.exts import db
from utils.digest_util import DigestUtil
from model.entity.user_model import UserModel

from api.rp import RP

bp_auth = Blueprint('oauth', __name__, url_prefix='/oauth')


@bp_auth.post('/login')
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    select = db.select(UserModel).where(UserModel.is_deleted == 0).where(UserModel.account == username)
    user = db.session.execute(select).scalar_one()
    print(user)
    print(type(user))
    if user is None:
        return {'error': "invalid_grant", 'error_description': "用户名或密码错误"}

    if DigestUtil.verify_sha256(password, user.password):

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        result = {
            "access_token": access_token,
            "refresh_token": refresh_token

        }

        return result
    else:
        return {'error': "invalid_grant", 'error_description': "用户名或密码错误"}


@bp_auth.post('/test')
@jwt_required()
def protected():
    # 使用 get_jwt_identity 访问当前用户的身份
    current_user = get_jwt_identity()
    return RP.data(current_user)
