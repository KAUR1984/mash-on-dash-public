from .search_engine_plugin import SearchEnginePlugin
import requests


class BingPlugin(SearchEnginePlugin):
    """
        A plugin that accesses the Bing Search API to retrieve information on the Web
        More information: https://azure.microsoft.com/pt-br/services/cognitive-services/bing-web-search-api/
    """
    _base_url = "https://api.cognitive.microsoft.com/bing/v7.0/"
    _subscription_key = None

    def configure(self, subscription_key):
        """
            Configure with a subscription key for Bing Search API

        :param subscription_key: signup for Bing Search in Cognitive Services to get your key
            https://azure.microsoft.com/pt-br/services/cognitive-services/bing-web-search-api/
        :type subscription_key: str

        """
        self._subscription_key = subscription_key

    def get_results(self, query, mkt, lang='en', count=2):
        """
            Gets last results for query from bing search


        :param query: search query term
            For advanced search operators for bing, see:
            https://www.bruceclay.com/blog/bing-yahoo-google-advanced-search-operators-guide/
        :type query: string
        :param mkt: required param. Country where the user wants to search.
            Valid codes are at this link:
            https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-web-api-v7-reference#market-codes
            Example: pt-BR
        :type mkt: string
        :param lang: not required. Interface language.
            Default = en. Possible values: http://www.mathguide.de/info/tools/languagecode.html
            Example: pt
        :type lang: string
        :param count: number of results. not required. default is 10. maximum: 50.
        :type count: int

        :return: result of webpages for query
        :rtype: list of dictionaries
            key: 'title'. value type: str
            description: the name of the webpage result

            key: 'snippet'. value type: str
            description: a snippet of text from the webpage result that describes its contents

            key: 'url'. value type: str
            description: the URL to the webpage

        """
        if not type(query) is str:
            raise TypeError(
                f"Parameter 'query' received is of type {type(query)}. This parameter must be an instance of string.")
        if not type(mkt) is str:
            raise TypeError(
                f"Parameter 'mkt' received is of type {type(mkt)}. This parameter must be an instance of string.")
        if not type(lang) is str:
            raise TypeError(
                f"Parameter 'lang' received is of type {type(lang)}. This parameter must be an instance of string.")
        if not type(count) is str:         # TODO should be "int" instead of "str"
            raise TypeError(
                f"Parameter 'count' received is of type {type(count)}. This parameter must be an instance of int.")

        headers = {"Ocp-Apim-Subscription-Key": self._subscription_key}
        params = {"q": query, "count": count, "mkt": mkt, "setLang": lang, "filterReuslts": "webpages",
                  "textDecorations": False}
        response = requests.get(self._base_url + 'search', headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        pages = search_results['webPages']['value']
        results = []
        for page in pages:
            result = {'title': page['name'], 'snippet': page['snippet'], 'url': page['url']}
            results.append(result)
        return results
