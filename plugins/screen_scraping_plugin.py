from abc import ABCMeta, ABC, abstractmethod
from workflow_manager.plugin import Plugin


class ScreenScrapingPlugin(ABC, Plugin):
    """An abstract class that represents a plugin (...)

    Attributes:
        scheduling: a boolean indicating whether the plugin execution can be scheduled.
        urls: a list of urls for running screen scraping
    """

    __metaclass__ = ABCMeta

    _urls = None

    def configure(self, urls):
        self._urls = urls

    @abstractmethod
    def do_scraping(self):
        pass
