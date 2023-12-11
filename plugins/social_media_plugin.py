from abc import ABCMeta, ABC, abstractmethod
from workflow_manager.plugin import Plugin


class SocialMediaPlugin(ABC, Plugin):
    """An abstract class that represents a plugin (...)

    Attributes:
        username: a string corresponding to the username of the social media.
        scheduling: a boolean indicating whether the plugin execution can be scheduled. default is False.
    """

    __metaclass__ = ABCMeta

    _username = None
    _tokens = None

    def configure(self, tokens):
        if type(tokens) is not dict:
            raise TypeError("tokens must be instance of dict")
        self._tokens = tokens

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def get_last_posts(self, count):
        pass

    @abstractmethod
    def search_posts(self, query, count):
        pass
