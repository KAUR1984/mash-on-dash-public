from abc import ABCMeta, ABC, abstractmethod
from workflow_manager.plugin import Plugin


class FilterPlugin(ABC, Plugin):
    """An abstract class that represents a plugin (...)

    """

    __metaclass__ = ABCMeta


    @abstractmethod
    def filter(self, data):
        pass
