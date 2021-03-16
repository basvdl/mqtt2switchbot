FROM python:3

RUN apt-get update && \
    apt-get install -y libbluetooth-dev && \
    apt-get install -y libboost-python-dev libboost-thread-dev && \
    apt-get install -y bluetooth

COPY . /switchbot_mqtt

#RUN pip install -r /switchbot_mqtt/requirements.txt
RUN pip install -e /switchbot_mqtt

COPY entrypoint.sh /root/.

ENTRYPOINT /root/entrypoint.sh
