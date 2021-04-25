import pytest


@pytest.fixture
def dummy_mac_address():
    return "fb:5f:a4:b9:96:4c"


@pytest.fixture
def dummy_set_topic(dummy_mac_address):
    return f"cover/switchbot-curtain/{dummy_mac_address}/set"


@pytest.fixture
def payload_open():
    return b"OPEN"


@pytest.fixture
def payload_close():
    return b"CLOSE"
