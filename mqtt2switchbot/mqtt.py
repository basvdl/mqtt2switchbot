import paho.mqtt.client
import logging
from mqtt2switchbot.switchbot_device import Curtain

_LOGGER = logging.getLogger(__name__)


class MQTTActor:
    def __init__(self):
        pass

    @staticmethod
    def _create_state_topic(topic: str) -> str:
        state_topic = topic.split("/")[:-1] + ["state"]
        return "/".join(state_topic)

    @staticmethod
    def _mqtt_publish(mqtt_client: paho.mqtt.client.Client, topic: str, message: str) -> None:
        mqtt_client.publish(topic, message)

    def _mqtt_callback(self,
                       mqtt_client: paho.mqtt.client.Client,
                       userdata: None,
                       message: paho.mqtt.client.MQTTMessage
                       ) -> None:
        _LOGGER.info(f"received topic={message.topic} payload={message.payload}")
        topic_split = message.topic.split("/")

        device_classes = {"switchbot-curtain": Curtain}

        try:
            device = device_classes[topic_split[2]](mac_address=topic_split[3])
            device.execute(message.payload)
        except Exception as e:
            _LOGGER.error(f"Unable to operate the device. Error {e}")
        else:
            _LOGGER.info(f"Updating the state. New state {device.get_state()}")
            self._mqtt_publish(mqtt_client, self._create_state_topic(message.topic), device.get_state())

    def mqtt_subscribe(self, mqtt_client: paho.mqtt.client.Client, topic: str) -> None:
        mqtt_client.subscribe(topic)
        mqtt_client.message_callback_add(sub=topic, callback=self._mqtt_callback)
