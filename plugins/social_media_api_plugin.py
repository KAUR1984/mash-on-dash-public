from abc import ABC, ABCMeta
from plugins.social_media_plugin import SocialMediaPlugin
from plugins.api_plugin import ApiPlugin


class SocialMediaApiPlugin(SocialMediaPlugin, ApiPlugin, ABC):
    """
        An abstract class that represents a plugin that connects with a rest API for getting social media data.

    """

    __metaclass__ = ABCMeta
