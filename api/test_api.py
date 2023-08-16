from flask import Blueprint, request, jsonify
from utils.mqtt import mqtt

bp_test = Blueprint('test', __name__, url_prefix='/test')


@bp_test.post('/publish_mqtt_message')
def publish_mqtt_message():
    request_data = request.get_json()
    publish_result = mqtt.publish(request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})
