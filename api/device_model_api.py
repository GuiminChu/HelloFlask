from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.exts import db
from utils.digest_util import DigestUtil
from utils.id_worker import idgen
from utils.func import Func
from model.entity.user_model import UserModel
from model.entity.devcie_model import DeviceModel
from model.rp import RP
from datetime import datetime
import json

bp_device_model = Blueprint('deviceModel', __name__, url_prefix='/device_model')


@bp_device_model.post('/save')
@jwt_required()
def save_device_model():
    """
    新增设备型号
    """

    model_name = request.json.get("modelName", None)
    if model_name is None or not isinstance(model_name, str):
        return RP.fail("请输入正确的型号名称")

    device_type = request.json.get("deviceType", None)
    if device_type is None or not isinstance(device_type, str):
        return RP.fail("请输入正确的设备类型")

    transport_type = request.json.get("transportType", None)
    if transport_type is None or not isinstance(transport_type, str):
        return RP.fail("请输入正确的协议类型")

    select = db.select(DeviceModel).where(DeviceModel.is_deleted == 0).where(DeviceModel.model_name == model_name)
    users = db.session.execute(select).all()

    if len(users) > 0:
        return RP.fail('型号名称重复')

    request_body = json.loads(request.get_data(as_text=True))
    new_model = DeviceModel.from_dict(Func.convert_camel_to_snake(request_body))
    new_model.id = idgen.next_id()
    # 使用 get_jwt_identity 访问当前用户的身份
    current_user = UserModel(**get_jwt_identity())
    new_model.create_user = current_user.id
    new_model.update_user = current_user.id

    now = datetime.now()
    new_model.create_time = now
    new_model.update_time = now

    new_model.save()
    return RP.data(new_model)


@bp_device_model.get('/list')
@jwt_required()
def get_dm_list():
    """
    获取设备型号列表
    """

    ds_list = db.session.execute(db.select(DeviceModel).order_by(DeviceModel.create_time)).scalars()
    print(type(ds_list))
    return RP.data([ds for ds in ds_list])
