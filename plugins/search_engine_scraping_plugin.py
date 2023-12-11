from abc import ABCMeta, ABC
from plugins.search_engine_plugin import SearchEnginePlugin
from plugins.screen_scraping_plugin import ScreenScrapingPlugin


class SearchEngineScrapingPlugin(SearchEnginePlugin, ScreenScrapingPlugin, ABC):
    """
        An abstract class that represents a plugin that does screen scraping on a search engine.

    """

    __metaclass__ = ABCMeta


