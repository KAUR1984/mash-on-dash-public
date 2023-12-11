from abc import ABC, ABCMeta
from plugins.social_media_plugin import SocialMediaPlugin
from plugins.screen_scraping_plugin import ScreenScrapingPlugin


class SocialMediaScrapingPlugin(SocialMediaPlugin, ScreenScrapingPlugin, ABC):
    """
        An abstract class that represents a plugin that does screen scraping on social medias.

    """

    __metaclass__ = ABCMeta
