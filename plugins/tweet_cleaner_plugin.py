from plugins.filter_plugin import FilterPlugin
from nltk.tokenize import WordPunctTokenizer
import re
from workflow_manager.plugin import Plugin


class TweetCleanerPlugin(FilterPlugin, Plugin):
    """
        A plugin that cleans up tweet content, buy removing links, hashtags and mentions

    """

    def filter(self, lst, target_key=None):
        """
            Clears the text of tweet by removing urls, hashtags and mentions

            :param lst: texts contained in tweets
            :type lst: list of strings or list of dictionaries
            :param target_key: a valid key that contains the tweet text.
                    if the data parameter is a list of dictionaries, this parameter is mandatory.
            :type target_key: string

            :return: data received and and the filter result, where dictionaries will have
            a key called 'clean tweet' with the result.
            :rtype: dictionary or list of dictionaries
        """

        if not type(lst) is list:
            raise TypeError(f"Parameter 'lst' is of type {type(lst)}. This parameter must be an instance of list.")
        list_of_str = all(isinstance(e, str) for e in lst)
        list_of_dicts = all(isinstance(e, dict) for e in lst)

        if not list_of_dicts and not list_of_str:
            raise TypeError(
                f"All elements of parameter 'lst' must be an instance of dictionary or string")
        if list_of_dicts and type(target_key) is not str:
            raise TypeError(f"Parameter 'target_key' is of type {type(target_key)}. This parameter must be an instance "
                            f"of string and is mandatory when parameter 'lst' is an list of dict.")
        results = []
        for element in lst:
            result = {}
            if list_of_str:
                clean_data = self.tweet_cleaner(element)
                result['clean tweet'] = clean_data
            elif list_of_dicts:
                clean_data = self.tweet_cleaner(element[target_key])
                element['clean tweet'] = clean_data
                result = element

            results.append(result)
        if len(results) > 0:
            return results
        else:
            return None

    def tweet_cleaner(self, text):
        """
            Cleans up tweet by removing mentions, urls and hashtags.

        :param text: tweet text
        :type text: string

        :return: tweet text cleaned
        :rtype: string
        """
        tok = WordPunctTokenizer()
        # clean mentions
        c1 = re.sub(r'@[A-Za-z0-9]+', '', text)
        # clean urls
        c2 = re.sub('https?://[A-Za-z0-9./]+', '', c1)
        # clean hashtags
        c3 = re.sub("[^a-zA-Z]", " ", c2)
        lower_case = c3.lower()
        words = tok.tokenize(lower_case)
        return (" ".join(words)).strip()
