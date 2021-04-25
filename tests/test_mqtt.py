import mqtt2switchbot.mqtt as victim


def test_create_state_topic(dummy_set_topic):
    result = victim.MQTTActor()._create_state_topic(dummy_set_topic)
    expected = "cover/switchbot-curtain/fb:5f:a4:b9:96:4c/state"

    assert expected == result
