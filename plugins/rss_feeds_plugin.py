from workflow_manager.plugin import Plugin
import feedparser


class RssFeedsPlugin(Plugin):
    """
        A plugin that reads rss feeds

        Attributes:
            _url_feed: a valid url of a rss feed

    """

    _url_feed = None

    def configure(self, url_feed):
        """
            Configures the plugin with url of rss feed

        :param url_feed: valid url for rss feed
        :return: string
        """
        if not type(url_feed) is str:
            raise TypeError(
                f"Parameter 'url_feed' is of type {type(url_feed)}. This attribute must be an instance of string.")
        self._url_feed = url_feed

    def get_articles(self):
        """
            Gets articles from a RSS feed

        :return: articles from RSS feed
        :rtype: list of dictionaries
            possible keys:
                title: article title
                summary: article summary
                link: link to the article
                published: date of publication of articles
        """
        if not self._url_feed:
            raise RuntimeError("No 'url_feed' found. Please, call configure before usage. ")
        results = []
        feed = feedparser.parse(self._url_feed)
        for entry in feed['entries']:
            result = {}
            if 'title' in entry:
                result['title'] = entry['title']
            if 'summary' in entry:
                result['summary'] = entry['summary']
            if 'link' in entry:
                result['link'] = entry['link']
            if 'published' in entry:
                result['published'] = entry['published']
            results.append(result)

        return results
