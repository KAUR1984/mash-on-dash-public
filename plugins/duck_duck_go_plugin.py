from plugins.search_engine_scraping_plugin import SearchEngineScrapingPlugin
import requests
import re
from bs4 import BeautifulSoup


class DuckDuckGoPlugin(SearchEngineScrapingPlugin):

    """ This plugin implements a screen scraping for Duck Duck Go search engine"""
    _url = None

    def get_results(self, query):
        """
            Gets the first page result from DuckDuckGo search

        :param query: query for search
        :type query: string
        :return: results
        :rtype: list of dictionaries
        """
        if type(query) is not str:
            raise TypeError(f"Parameter 'query' is of type {type(query)}. Must be of type string.")

        query = re.sub(' +', '+', query)
        self._url = 'https://duckduckgo.com/html/?q={}'.format(query)
        return self._do_scraping(query)

    def do_scraping(self, query):
        """
            Changed the method signature to include query as a parameter. TODO

        :param query: query for search
        :type query: string
        :return: results
        :rtype: list of dictionaries
        """
        page = requests.get(self._url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            div_results = soup.select('div .result')
            results = []
            for div_result in div_results:
                div_result.find('div.no-results')
                result = {}
                result['title'] = div_result.select('h2.result__title a')[0].text
                if result['title'] == 'No  results.':
                    break
                result['snippet'] = div_result.select('a.result__snippet')[0].text
                result['url'] = div_result.find('a', class_='result__snippet').get('href')
                results.append(result)

            return results
        else:
            raise RuntimeError(f"Error for {query}: {page.status_code}")
