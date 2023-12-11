from .filter_plugin import FilterPlugin
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from workflow_manager.plugin import Plugin


class StopwordsPlugin(FilterPlugin, Plugin):
    """
        A plugin that cleans up textual data by removing the stopwords found in it

    Attributes:
        _lang: text language

    """

    _lang = None

    def configure(self, lang):
        """ Configure the plugin with text language

            :param lang: text language
            :type lang: string
        """

        if type(lang) is not str:
            raise TypeError(f"Parameter 'lang' is of type {type(lang)}. This parameter must be an instance of list.")
        self._lang = lang

    def filter(self, lst, target_key=None):
        """
            Clears the textual data by removing the stopwords found on it.

            :param lst: texts. the language of the text must be consistent with the configured language.
            :type lst: list of strings or list of dictionaries
            :param target_key: a valid key that contains the text.
                    if the data parameter is a list of dictionaries, this parameter is mandatory.
            :type target_key: string

            :return: data received and and the filter result, where dictionaries will have
            a key called 'clean data' with the result.
            :rtype: dictionary or list of dictionaries
        """
        if not self._lang:
            raise RuntimeError("There isn't 'lang' configured for this plugin. "
                               "Please, call configure before usage.")
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
                clean_data = self.remove_stopwords(element)
                result['clean data'] = clean_data
            elif list_of_dicts:
                clean_data = self.get_sentiment(element[target_key])
                element['clean data'] = clean_data
                result = element

            results.append(result)
        if len(results) > 0:
            return results
        else:
            return None

    def remove_stopwords(self, text):
        """
            Clears strings by removing the stopwords found on it

            :param text: texts. the language of the text must be consistent with the configured language.
            :type text: string

            :return: the filter result
            :rtype: string
        """
        if type(text) is not str:
            raise TypeError(f"Parameter 'text' is of type {type(text)}. This parameter must be an instance of string.")
        stop_words = set(stopwords.words(self.lang))
        text = " ".join(text)
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        if filtered_sentence:
            return " ".join(filtered_sentence)
        else:
            return None
