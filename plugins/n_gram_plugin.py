from workflow_manager.plugin import Plugin
from nltk.util import ngrams
from nltk import FreqDist


class NGramPlugin(Plugin):
    """
        A plugin to extract and work with n-grams

    """

    def extract_ngram_frequencies(self, data, n=1):
        """
            Extracts n-gram frequencies for text

        :param data: text to extract n-grams frequencies
        :type data: string or list of strings
        :param n: size of n-gram. default is 1
        :type n: int

        :return: frequency by grams
        :rtype: list of tuples (gram, frequency)

        """
        if not type(data) in (str, list):
            raise TypeError(f"Parameter 'data' is of type {type(data)}, must be a instance of string or list.")
        if type(data) is list:
            if not all(isinstance(s, str) for s in data):
                raise TypeError(f"Parameter 'data' has elements that aren't instance of string.")
            grams = ngrams(data, n)
        elif type(data) is str:
            grams = ngrams(data.split(), n)
        fdist = FreqDist(grams)
        return [(k, fdist[k]) for k in sorted(fdist, key=fdist.get, reverse=True)]
