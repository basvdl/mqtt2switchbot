import mqtt2switchbot.switchbot_device as victim


def test_command_open(dummy_mac_address, payload_open):
    result = victim.Curtain(mac_address=dummy_mac_address)._command(payload=payload_open)
    expected = [0x57, 0x0f, 0x45, 0x01, 0x05, 0xff, 0x00]

    assert result == expected


def test_command_position(dummy_mac_address):
    position = 87
    result = victim.Curtain(mac_address=dummy_mac_address)._command(payload=position)
    expected = [0x57, 0x0f, 0x45, 0x01, 0x05, 0xff, position]

    assert result == expected


def test_command_close_silent(dummy_mac_address, payload_close):
    result = victim.Curtain(mac_address=dummy_mac_address, silent_mode=True)._command(payload=payload_close)
    expected = [0x57, 0x0f, 0x45, 0x01, 0x05, 0x01, 0x64]

    assert result == expected
