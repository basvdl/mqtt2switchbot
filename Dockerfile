FROM python:3

RUN apt-get update && \
    apt-get install -y libbluetooth-dev && \
    apt-get install -y libboost-python-dev libboost-thread-dev && \
    apt-get install -y bluetooth

RUN pip install --no-cache-dir paho-mqtt==1.5.1 bleak==0.10.0

COPY . /switchbot_mqtt

COPY entrypoint.sh /root/.

ENTRYPOINT /root/entrypoint.sh
