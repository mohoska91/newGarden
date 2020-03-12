from abc import abstractmethod
from typing import List

from connect.gardensession import GardenSession
from connect.rpiconnector import RaspberryPIConnector
from gardener import utils as utility
from gardener.loggingutils import get_logger
from gardener.sensor_factory import RawSensing
from model import TimedRequirement, SensedRequirement, GardenTool, Requirement, PluginCore, TimedPluginCore, \
    SensedPluginCore, Lifeline


class Plugin:

    def __init__(self, plugin_core: PluginCore, connector: RaspberryPIConnector):
        self._logger = get_logger(self.__class__.__name__)
        self._state = False
        self._connector = connector
        self._plugin_core = plugin_core
        self._setup_plugin()

    @abstractmethod
    def _setup_plugin(self, *args):
        pass

    @abstractmethod
    def control(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class TimerPlugin(Plugin):

    def __init__(self, timed_requirement: TimedRequirement, plugin_core: TimedPluginCore, connector: RaspberryPIConnector):
        super().__init__(plugin_core, connector)
        self._timed_requirement = timed_requirement
        self._tool = self._plugin_core.tool
        self._connector.setup_gpio(self._tool.gpio, self._state)

    def control(self):
        self._control_by_time()

    def _control_by_time(self):
        state = any(
            utility.is_time_in_range(
                interval.start_time,
                utility.get_now().time(),
                interval.end_time
            )
            for interval in self._timed_requirement.time_intervals
        )
        if state != self._state:
            print(self.__class__, self._tool.name, " control")
            self._connector.set_gpio(self._tool.gpio, state)
            self._state = state

    def stop(self):
        self._connector.set_gpio(self._tool.gpio, False)


class SensorPlugin(Plugin):
    def __init__(self, sensed_requirement: SensedRequirement, plugin_core: SensedPluginCore, connector: RaspberryPIConnector):
        super().__init__(plugin_core, connector)
        self._sensed_requirement = sensed_requirement
        self._tool = self._plugin_core.tool
        self._sensor = self._plugin_core.sensor
        self._connector.setup_gpio(self._tool.gpio, self._state)

    def control(self):
        self._control_by_sensor()

    def _control_by_sensor(self):
        sensed = RawSensing.sense(self._sensor)
        state = sensed <= self._sensed_requirement.min_value
        if state != self._state:
            print(self.__class__, self._tool.name,  " control")
            self._connector.set_gpio(self._tool.gpio, state)
            self._state = state

    def stop(self):
        self._connector.set_gpio(self._tool.gpio, False)


def get_plugins(lifeline_id: int, session: GardenSession, rpi_connector: RaspberryPIConnector):
    lifeline = session.get_lifeline_by_id(lifeline_id)
    return [
        _get_plugin(requirement, session, rpi_connector)
        for requirement in lifeline.requirements
    ]


def _get_plugin(requirement: Requirement, session: GardenSession, rpi_connector: RaspberryPIConnector):
    plugincore = session.get_plugincore_by_requirement(requirement)
    if isinstance(plugincore, SensedPluginCore):
        return SensorPlugin(requirement, plugincore, rpi_connector)
    return TimerPlugin(requirement, plugincore, rpi_connector)