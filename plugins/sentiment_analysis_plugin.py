from .filter_plugin import FilterPlugin
from workflow_manager.plugin import Plugin
from textblob import TextBlob


class SentimentAnalysisPlugin(FilterPlugin):
    """
        A plugin for textual sentiment analysis

    """

    def filter(self, lst, target_key=None):
        """
            Gets a textual sentiment analysis for a set of text data.
            Analysis is only possible for texts in English.
            Sentiments are described as 'positive', 'negative' and 'neutral'

            :param lst: texts in english for sentiment analysis
            :type lst: list of strings or list of dictionaries
            :param target_key: a valid key that contains the text.
                    if the data parameter is a list of dictionaries, this parameter is mandatory.
            :type target_key: string

            :return: data received and sentiment analysis result, where dictionaries will have
            a key called 'sentiment' with the result
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
                sentiment_result = self.get_sentiment(element)
                result['sentiment'] = sentiment_result
            elif list_of_dicts:
                sentiment_result = self.get_sentiment(element[target_key])
                element['sentiment'] = sentiment_result
                result = element

            results.append(result)
        if len(results) > 0:
            return results
        else:
            return None

    def get_sentiment(self, text):
        """
            Gets a textual sentiment analysis.
            Analysis is only possible for text in english.
            Sentiments are described as 'positive', 'negative' and 'neutral'

        :param text: text in english
        :type text: str

        :return: sentiment analysis result
        :rtype: string
        """
        if type(text) is not str:
            raise TypeError(f"Parameter 'text' is of type {type(text)}. This parameter must be an instance of string.")
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
