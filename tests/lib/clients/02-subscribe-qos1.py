import paho.mqtt.client as mqtt

from tests.paho_test import get_test_server_port, loop_until_keyboard_interrupt


def on_connect(mqttc, obj, flags, rc):
    assert rc == 0, f"Connect failed ({rc})"
    mqttc.subscribe("qos1/test", 1)


def on_subscribe(mqttc, obj, mid, granted_qos):
    mqttc.disconnect()


mqttc = mqtt.Client("subscribe-qos1-test", clean_session=True)
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect("localhost", get_test_server_port())
loop_until_keyboard_interrupt(mqttc)
