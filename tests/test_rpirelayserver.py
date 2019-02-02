import sys
import os
from pathlib import Path
p = Path.home() / 'rpirelayserver' / 'rpirelayserver'
sys.path.append(str(p.resolve())) # '/home/pi/rpirelayserver/rpirelayserver'
print(sys.path)
import rpirelayserver as rpi


class TestRelayStatus:
    pass


class TestGetRelayStatus:
    pass


class TestUpdateRelayState:
    pass


class TestSetRelayStates:
    pass


class TestProcessData:
    pass


class TestUnpackData:
    # Test payload b'\x008{"message_type": "ChannelRequest", "message_length": 10}[4, false]'
    def test_unpack_data_returns_message_length(self):
        data = rpi.unpack_data(b'{"message_type": "ChannelRequest", "message_length": 10}')
        assert isinstance(data, dict)

