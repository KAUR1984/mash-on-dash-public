from abc import ABC, ABCMeta
from plugins.search_engine_plugin import SearchEnginePlugin
from plugins.api_plugin import ApiPlugin


class SearchEngineApiPlugin(SearchEnginePlugin, ApiPlugin, ABC):
    """
        An abstract class that represents a plugin that connects with a rest API for an search engine.

    """

    __metaclass__ = ABCMeta
