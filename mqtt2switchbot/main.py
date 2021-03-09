import argparse
import logging
import typing
import paho.mqtt.client
from mqtt2switchbot.mqtt import MQTTActor
from mqtt2switchbot.config import LOG_LEVEL, COMMAND_TOPIC

_LOGGER = logging.getLogger(__name__)


def mqtt_on_connect(
        mqtt_client: paho.mqtt.client.Client,
        user_data: typing.Any,
        flags: typing.Dict,
        return_code: int,
) -> None:
    _LOGGER.info(f"Subscribing to MQTT topic {COMMAND_TOPIC}")
    MQTTActor().mqtt_subscribe(mqtt_client=mqtt_client, topic=COMMAND_TOPIC)


def main(mqtt_host: str, mqtt_port: str) -> None:
    mqtt_client = paho.mqtt.client.Client()
    _LOGGER.info(f"Connecting to MQTT broker {mqtt_host}:{mqtt_port}")
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.connect(host=mqtt_host, port=mqtt_port)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    logging.basicConfig(
        level=LOG_LEVEL
    )

    argparser = argparse.ArgumentParser(
        description="MQTT client controlling SwitchBot"
    )

    argparser.add_argument("--mqtt-host", type=str, required=True)
    argparser.add_argument("--mqtt-port", type=int, default=1883)
    args = argparser.parse_args()

    main(args.mqtt_host, args.mqtt_port)
