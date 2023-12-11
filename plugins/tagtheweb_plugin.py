import requests
from workflow_manager.plugin import Plugin

try:
    import json
except ImportError:
    import simplejson as json


class TagthewebPlugin(Plugin):
    """
        Classify content on web based on the concepts of Wisdom of the Crowds and Linked Open Data.

        Official website: http://tagtheweb.com.br/
        Documentation: https://documenter.getpostman.com/view/1071275/tagtheweb/77bC7Kn

        Attributes:
            tagtheweb_endpoint: endpoint for API
            _language: language of text.
                    valid values: en, de, nl, fr, it, ru, es, pt, hu, tr
                    default is 'en'.
            _depth: depth level of wikipedia categorization. default is 0.

    """

    _endpoint = 'http://tagtheweb.com.br/wiki/getFingerPrint.php?language={}&text={}&depth={}&normalize=false'

    _language = None
    _depth = None

    def configure(self, language='en', depth=0):
        """
            Configures the plugin with

            :param language: language of text.
                    valid values: en, de, nl, fr, it, ru, es, pt, hu, tr
                    default is 'en'.
            :param depth: depth level of wikipedia categorization. default is 0.
        """
        self._language = language
        self._depth = depth

    def generate_finger_print(self, text):
        """
            Given text, returns the percentual distribution of topics along the 19 WIkipedia topic categories.
            (extracted from the official documentation, see more:
            https://documenter.getpostman.com/view/1071275/tagtheweb/77bC7Kn)

            :type text:
            :return: tuple with percentual distribution per topic
            :rtype: list of tuples
        """

        if type(text) is not str:
            raise TypeError(f"Parameter 'text' is of type {type(text)}. This parameter must be an instance of string.")
        request_uri = self.tagtheweb_endpoint.format(self._language, text, self._depth)
        response = requests.get(request_uri)
        dict_response = json.loads(response.text)

        if dict_response:
            items = ((value, key) for (key, value) in dict_response.items())
            return sorted(items, reverse=True)
        else:
            return None
