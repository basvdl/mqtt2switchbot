#!/bin/bash

service dbus start
service bluetooth start

python /switchbot_mqtt/switchbot_mqtt/main.py --mqtt-host 192.168.178.122
