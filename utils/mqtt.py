# flask_mqtt 1.1.1 版本有问题
# https://flask-mqtt.readthedocs.io/en/latest/index.html
from utils.my_flask_mqtt import Mqtt
from utils.logger import logger

mqtt = Mqtt()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info('MQTT ==> Connected successfully')

        # 订阅主题
        mqtt.subscribe('home/my_topic')
    else:
        logger.error('MQTT ==> Bad connection. Code:', rc)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    logger.info('MQTT ==> Received message on topic: {topic} with payload: {payload}'.format(**data))


def publish_msg(topic, msg):
    publish_result = mqtt.publish(topic, msg)

    if publish_result[0] == 0:
        logger.info("Published topic {0}: {1}".format(topic, msg))
    else:
        logger.error("Error {0} publishing topic {1}".format(publish_result[0], topic))
