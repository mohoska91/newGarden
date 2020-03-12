from json import dumps, loads
from typing import Optional

from redis import Redis

START_MESSAGE_ID = "start"
STOP_MESSAGE_ID = "stop"
_ACTION = "action"
_LIFELINE_ID = "lifeline_id"


class GardenerMessage:
    def __init__(self, action: str, lifeline_id: int):
        self._lifeline_id = lifeline_id
        self._action = action

    @property
    def lifeline_id(self):
        return self._lifeline_id

    @property
    def action(self):
        return self._action

    def to_dict(self):
        return {
            _ACTION: self.action,
            _LIFELINE_ID: str(self.lifeline_id)
        }

    def to_json(self):
        return dumps(self.to_dict())


class GardenerStartMessage(GardenerMessage):
    def __init__(self, lifeline_id: int):
        super().__init__(START_MESSAGE_ID, lifeline_id)


class GardenerStopMessage(GardenerMessage):
    def __init__(self, lifeline_id: int):
        super().__init__(STOP_MESSAGE_ID, lifeline_id)


class GardenerMessageFactory:
    _MESSAGE_MAP = {
        START_MESSAGE_ID: GardenerStartMessage,
        STOP_MESSAGE_ID: GardenerStopMessage
    }
    @classmethod
    def get_message(cls, msg_id: str, lifeline_id: int) -> GardenerMessage:
        return cls._MESSAGE_MAP[msg_id](lifeline_id)


class GardenerMessenger:

    _MESSAGE = "simple_message"

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._redis = Redis(host, port)

    def put_message(self, msg: GardenerMessage):
        self._redis.rpush(self._MESSAGE, msg.to_json())

    def pop_message(self) -> Optional[GardenerMessage]:
        data = self._redis.lpop(self._MESSAGE)
        data = data and loads(data)
        return data and GardenerMessageFactory.get_message(data[_ACTION], int(data[_LIFELINE_ID]))
