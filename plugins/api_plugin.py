from abc import ABC, ABCMeta, abstractmethod
from workflow_manager.plugin import Plugin


class ApiPlugin(ABC, Plugin):
    """
        An abstract class that represents a plugin that connects with a rest API.

    """

    __metaclass__ = ABCMeta

    _tokens = None

    def configure(self, tokens):
        """


        :param tokens:
        :return:
        """
        self._tokens = tokens

    @abstractmethod
    def authenticate(self):
        """

        :return:
        """
        pass
