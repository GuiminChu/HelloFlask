from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.exts import db
from utils.digest_util import DigestUtil
from utils.id_worker import idgen
from utils.func import Func
from model.entity.user_model import UserModel
from model.entity.devcie_model import DeviceModel, DeviceSwitch
from model.rp import RP
from datetime import datetime
import json

bp_device_switch = Blueprint('deviceSwitch', __name__, url_prefix='/device_switch')


@bp_device_switch.post('/save')
@jwt_required()
def save_device_switch():
    model_id = request.json.get("modelId", None)
    if model_id is None or not isinstance(model_id, str):
        return RP.fail("请选择正确的产品型号")

    device_name = request.json.get("deviceName", None)
    if device_name is None or not isinstance(device_name, str):
        return RP.fail("请输入正确的设备名称")

    device_sn = request.json.get("deviceSn", None)
    if device_sn is None or not isinstance(device_sn, str):
        return RP.fail("请输入正确的设备序列号")

    select = db.select(DeviceSwitch).where(DeviceSwitch.is_deleted == 0).where(DeviceSwitch.device_sn == device_sn)
    device_list = db.session.execute(select).all()

    if len(device_list) > 0:
        return RP.fail('设备序列号重复')

    request_body = json.loads(request.get_data(as_text=True))
    new_switch = DeviceSwitch.from_dict(Func.convert_camel_to_snake(request_body))
    new_switch.id = idgen.next_id()
    # 使用 get_jwt_identity 访问当前用户的身份
    current_user = UserModel(**get_jwt_identity())
    new_switch.create_user = current_user.id
    new_switch.update_user = current_user.id

    now = datetime.now()
    new_switch.create_time = now
    new_switch.update_time = now

    new_switch.save()
    return RP.data(new_switch)
