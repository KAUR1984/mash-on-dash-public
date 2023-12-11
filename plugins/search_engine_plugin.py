from abc import ABCMeta, ABC, abstractmethod
from workflow_manager.plugin import Plugin


class SearchEnginePlugin(ABC, Plugin):
    """An abstract class that represents a plugin (...)

    Attributes:
        scheduling: a boolean indicating whether the plugin execution can be scheduled.
    """

    __metaclass__ = ABCMeta

    def configure(self):
        pass

    @abstractmethod
    def get_results(self, query):
        pass
