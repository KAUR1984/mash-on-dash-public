from plugins.social_media_plugin import SocialMediaPlugin
from tweepy import OAuthHandler, API, TweepyException, TooManyRequests

try:
    import json
except ImportError:
    import simplejson as json
import itertools


class TwitterPlugin(SocialMediaPlugin):
    """
        This plugin uses Tweepy package for getting data from Twitter API

    """
    tokens_required = ('access_token', 'access_secret', 'consumer_key', 'consumer_secret')

    _twitter_instance = None
    _expected_exception = (TweepyException, TooManyRequests)              # TODO changed the imports.

    def configure(self, tokens):
        """
            Configures plugin with tokens
        :param tokens: tokens of user
        :type tokens: dict
        :return: none
        """
        self.validate_tokens(tokens)
        self.set_expected_exception(self._expected_exception)
        SocialMediaPlugin.configure(self, tokens)

    def validate_tokens(self, tokens):
        """
            Validate tokens before configuring the plugin
        :param tokens: tokens of user
        :type tokens: dict
        :raise TypeError, ValueError, KeyError
        """
        missing_tokens = [token_required for token_required in self.tokens_required if
                          token_required not in tokens.keys()]
        invalid_tokens = [token_type for token_type in tokens.keys() if token_type not in self.tokens_required]
        if type(tokens) is not dict:
            raise TypeError("tokens must be instance of dict")
        if len(invalid_tokens) != 0:
            format_keys = ', '.join(invalid_tokens)
            raise ValueError(f"Invalid(s) token(s) in the 'tokens' argument: '{format_keys}'")
        if len(missing_tokens) != 0:
            format_keys = ', '.join(missing_tokens)
            raise KeyError(f"Missing token(s) in the 'tokens' argument: '{format_keys}'")

    def authenticate(self):
        """"
            Authenticates the api instance
        """
        if not self._tokens:
            raise AttributeError("There isn't tokens for this plugin. Please, call configure before usage.")
        auth = OAuthHandler(self._tokens['consumer_key'], self._tokens['consumer_secret'])
        auth.set_access_token(self._tokens['access_token'], self._tokens['access_secret'])

        self._twitter_instance = API(auth)

    def get_last_posts(self, user_name, count=1, only_text=True):
        """
            Get a specific number of tweets from an user

            Keyword arguments:
                :param count: number of tweets (default is 1)
                :type count: int
                :param user_name:
                :type user_name: str
                :param only_text - defines whether the return is a list of tweets or a list of dictionaries with
            complementary information: user, tweet id, date, tweet text and retweet_count.
                :type only_text: bool
        """

        results = []

        if self._twitter_instance is None:
            self.authenticate()
        t = self._twitter_instance

        tweets = t.user_timeline(screen_name=user_name, count=count, tweet_mode='extended')
        for tweet in tweets:
            if only_text:
                results.append(tweet.full_text.replace("\n", ""))
            else:
                result = {}
                result['user'] = tweet.user.screen_name
                result['tweet_id'] = tweet.id_str
                result['date'] = tweet.created_at
                result['text'] = tweet.full_text.replace("\n", "")
                result['retweet_count'] = tweet.retweet_count
                results.append(result)
        return results

    def search_posts(self, query, count=1, only_text=True):
        """Get a specific number of tweets

            Arguments:
                :param query: a string that contains the search query
                :type query: str
            Keyword arguments:
                :param count: number of tweets (default is 1)
                :type count: int
                :param only_text: defines whether the return is a list of tweets or a list of dictionaries with
            complementary information: user, tweet id, date, tweet text and retweet_count.
                :type only_text: bool

            :return list or list of dictionaries
            :rtype list
        """

        results = []

        if self._twitter_instance is None:
            self.authenticate()
        t = self._twitter_instance

        tweets = t.search_tweets(q=query, lang='en', count=count, tweet_mode='extended')     #TODO replaced `search` with `search_tweets`
        for tweet in tweets:
            if only_text:
                results.append(tweet.full_text.replace("\n", ""))
            else:
                result = {}
                result['user'] = tweet.user.screen_name
                result['tweet_id'] = tweet.id_str
                result['date'] = tweet.created_at
                result['text'] = tweet.full_text.replace("\n", "")
                result['retweet_count'] = tweet.retweet_count
                results.append(result)
        return results

    def _paginate(self, iterable, page_size):
        """
            This method does paginating the list of ids to not exceed the rate limit of the method "statuses_lookup"

          :param iterable: an iterable for paginating
          :type iterable:  iterable

          :param page_size: page size
          :type page_size: int

         """
        while True:
            i1, i2 = itertools.tee(iterable)
            iterable, page = (itertools.islice(i1, page_size, None),
                              list(itertools.islice(i2, page_size)))
            if len(page) == 0:
                break
            yield page

    def get_tweets_by_ids(self, ids, rt=False):
        """
            Given a list of tweet ids, returns the corresponding tweets

            Arguments:
                :param ids - list of tweet ids
                :type ids - list

            :return list of tweets
            :rtype list
        """
        total_result = []
        if not ids:
            return []
        t = self._twitter_instance
        for page in self._paginate(ids, 90):
            result = t.lookup_statuses(page, tweet_mode='extended')           #TODO replaced `statuses_lookup` with `lookup_statuses`.
            if rt:
                total_result += [r._json for r in result]
            else:
                total_result += [r._json for r in result if not 'retweeted_status' in r._json]
        return total_result
