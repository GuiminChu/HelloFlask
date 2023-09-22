from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.exts import db
from utils.digest_util import DigestUtil
from utils.id_worker import idgen
from utils.func import Func
from utils.http_util import HttpUtil
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

    # 查询物联网平台是否已经添加该设备
    d1 = HttpUtil.get_device_detail(new_switch.id)
    if d1 is None:
        HttpUtil.save_device(new_switch.id, model_id, new_switch.device_name, new_switch.device_sn)

    return RP.data(new_switch)


@bp_device_switch.get('/detail/<int:ds_id>')
@jwt_required()
def device_switch_detail(ds_id):
    """
    获取智能开关详情
    """

    device_switch = db.session.query(DeviceSwitch).filter(DeviceSwitch.id == ds_id).first()
    if device_switch:
        return RP.data(device_switch)
    else:
        return RP.fail("设备不存在")


@bp_device_switch.get('/list')
@jwt_required()
def get_ds_list():
    """
    获取智能开关列表
    """

    # ds_list = db.session.execute(db.select(DeviceSwitch).order_by(DeviceSwitch.create_time.desc())).scalars()
    ds_list = db.session.execute(db.select(DeviceSwitch).order_by(DeviceSwitch.create_time)).scalars()
    # return RP.data([ds.to_dict() for ds in ds_list])
    return RP.data([ds for ds in ds_list])


@bp_device_switch.post('/switch')
@jwt_required()
def ds_switch():
    """
    打开或关闭开关

    id: 设备id

    way: 0 全部路数，其他值代表具体开关几

    op: 1 打开 0关闭
    """

    # 这是 str 格式
    d = request.get_data(as_text=True)
    print(type(d))
    print(d)
    print('----')

    # dict 格式
    j = request.get_json()
    print(type(j))
    print(j)
    print('----')

    data = json.loads(request.get_data(as_text=True))
    print(data)
    ds_id = data.get('id')
    if not ds_id:
        return RP.fail('id不能为空')

    way: int = data.get('way')
    op: int = data.get('op')

    ds_entity: DeviceSwitch = db.session.query(DeviceSwitch).filter(DeviceSwitch.id == ds_id).first()
    print(ds_entity)

    if ds_entity is None:
        return RP.fail("设备不存在")

    topic: str = f'/switch/{ds_entity.device_sn}/set'

    # 关闭操作
    if op == 0:
        # 全关
        if way == 0:
            payload = 'qg'
        # 分路关
        else:
            payload = f'a{way}'
    # 打开操作
    else:
        # 全开
        if way == 0:
            payload = 'qk'
        # 分路开
        else:
            payload = f'b{way}'

    result: bool = HttpUtil.send_device_message(str(ds_entity.id), topic, payload)
    if result:
        return RP.success('操作成功')
    else:
        return RP.fail('操作失败')
