from json import dumps, loads
from typing import Optional

from redis import Redis


class GardenerConfig:
    _RUNNING_LIFELINE_ID = "rlid"

    def __init__(self, config: Optional[dict]):
        self._config = config or {}

    @property
    def config(self) -> dict:
        return self._config

    @property
    def running_lifeline_id(self) -> int:
        return self._config.get(self._RUNNING_LIFELINE_ID, None)

    @running_lifeline_id.setter
    def running_lifeline_id(self, lifeline_id: Optional[int]):
        self._config[self._RUNNING_LIFELINE_ID] = lifeline_id

    def is_empty(self) -> bool:
        return self._config != {}


class ConfigDBConnector:

    _GARDENER_CONFIG = "gardener_config"

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._redis = Redis(host, port)
        self._gardener_config = GardenerConfig(self._get_raw_gardener_config())

    def save_running_lifeline_id(self, lifeline_id: int):
        self._set_lifeline_config(lifeline_id)

    def remove_running_lifeline_id(self, lifeline_id: int):
        if self.get_running_lifeline_id() != lifeline_id:
            #TODO error raising
            return
        self._set_lifeline_config(None)

    def get_running_lifeline_id(self) -> int:
        return self._gardener_config.running_lifeline_id

    def _set_lifeline_config(self, lifeline_id: Optional[int]):
        self._gardener_config.running_lifeline_id = lifeline_id
        self._save_raw_gardener_config()

    def _save_raw_gardener_config(self):
        return self._redis.set(self._GARDENER_CONFIG, dumps(self._gardener_config.config))

    def _get_raw_gardener_config(self):
        loaded = self._redis.get(self._GARDENER_CONFIG)
        return loaded and loads(loaded)
