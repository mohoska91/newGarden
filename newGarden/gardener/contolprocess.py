from threading import Lock
from time import sleep
from typing import Optional

from connect.gardensession import GardenSessionProvider, GardenSession
from connect.gardenerconfigconnector import ConfigDBConnector
from connect.messanger import GardenerMessenger, GardenerMessage, START_MESSAGE_ID, STOP_MESSAGE_ID
from connect.rpiconnector import RaspberryPIConnector
from gardener.controller import LifelineController
from gardener.loggingutils import get_logger
from gardener.plugin import get_plugins


class ConnectorContext:
    def __init__(self, datadbconnector: GardenSessionProvider, config_connector: ConfigDBConnector,
                 messanger: GardenerMessenger, rpi_connector: RaspberryPIConnector):
        self._data_session_provider = datadbconnector
        self._config = config_connector
        self._messenger = messanger
        self._rpi = rpi_connector

    @property
    def data_session(self) -> GardenSession:
        return self._data_session_provider.provide_session()

    @property
    def config(self) -> ConfigDBConnector:
        return self._config

    @property
    def rpi(self) -> RaspberryPIConnector:
        return self._rpi

    @property
    def messenger(self) -> GardenerMessenger:
        return self._messenger


class ControlProcess:

    def __init__(self, connector_context: ConnectorContext):
        self._run = True
        self._lock = Lock()
        self._connector_context = connector_context
        self._controller = None
        self._logger = get_logger(self.__class__.__name__)

    def run_control(self):
        self._run = True
        while self._run:
            message = self._connector_context.messenger.pop_message()
            if message:
                self._set_config_by_message(message)
            self._controller = self._get_controller_by_id(self._connector_context.config.get_running_lifeline_id())
            if self._controller:
                self._controller.control()
            sleep(1)

    def _get_controller_by_id(self, lifeline_id: int) -> Optional[LifelineController]:
        if lifeline_id is None:
            return None
        if self._is_the_same_lifeline(lifeline_id):
            return self._controller
        return LifelineController(
            lifeline_id,
            get_plugins(
                lifeline_id,
                self._connector_context.data_session,
                self._connector_context.rpi
            )
        )

    def _set_config_by_message(self, message: GardenerMessage):
        if message.action == START_MESSAGE_ID:
            self._connector_context.config.save_running_lifeline_id(message.lifeline_id)
        if message.action == STOP_MESSAGE_ID:
            self._connector_context.config.remove_running_lifeline_id(message.lifeline_id)

    def _is_the_same_lifeline(self, lifeline_id: int):
        return self._controller is not None and self._controller.lifeline_id == lifeline_id

    def stop_control(self):
        with self._lock:
            self._run = False
