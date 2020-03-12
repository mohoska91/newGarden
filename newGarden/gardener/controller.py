from typing import List

from gardener.plugin import Plugin


class LifelineController:
    def __init__(self, lifeline_id, plugins: List[Plugin]):
        self._lifeline_id = lifeline_id
        self._plugins = plugins

    @property
    def lifeline_id(self):
        return self._lifeline_id

    def control(self):
        for plugin in self._plugins:
            plugin.control()

    def stop(self):
        for plugin in self._plugins:
            plugin.stop()
