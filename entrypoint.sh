#!/bin/bash

service dbus start
service bluetooth start

python /switchbot_mqtt/mqtt2switchbot/main.py --mqtt-host 192.168.178.122
