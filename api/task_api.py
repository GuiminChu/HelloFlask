from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.exts import db
from model.entity.smart_task_model import SmartTaskModel
from model.rp import RP
from utils.id_worker import idgen
from utils.func import Func
from datetime import datetime
import json
from utils.jobs import scheduler, test_job_3

bp_task = Blueprint('task', __name__, url_prefix='/task')


@bp_task.post('/save')
@jwt_required()
def save_task():
    model_name = request.json.get("modelName", None)
    if model_name is None or not isinstance(model_name, str):
        return RP.fail("请输入正确的型号名称")

    device_type = request.json.get("deviceType", None)
    if device_type is None or not isinstance(device_type, str):
        return RP.fail("请输入正确的设备类型")

    transport_type = request.json.get("transportType", None)
    if transport_type is None or not isinstance(transport_type, str):
        return RP.fail("请输入正确的协议类型")

    select = db.select(SmartTaskModel).where(SmartTaskModel.is_deleted == 0).where(
        SmartTaskModel.model_name == model_name)
    users = db.session.execute(select).all()

    if len(users) > 0:
        return RP.fail('型号名称重复')

    request_body = json.loads(request.get_data(as_text=True))
    new_model = SmartTaskModel.from_dict(Func.convert_camel_to_snake(request_body))
    new_model.id = idgen.next_id()
    # 使用 get_jwt_identity 访问当前用户的身份
    current_user = SmartTaskModel(**get_jwt_identity())
    new_model.create_user = current_user.id
    new_model.update_user = current_user.id

    now = datetime.now()
    new_model.create_time = now
    new_model.update_time = now

    new_model.save()
    return RP.data(new_model)


@bp_task.get('/test')
def test_task():
    job = scheduler.add_job(
        id="test_job_3",
        func=test_job_3,
        args=(3,),
        trigger="interval",
        seconds=3
        # replace_existing=True
    )
    return "Task scheduled"
