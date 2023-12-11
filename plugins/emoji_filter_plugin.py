from .filter_plugin import FilterPlugin
from workflow_manager.plugin import Plugin
import unicodedata
import emoji
import regex


class EmojiFilterPlugin(FilterPlugin, Plugin):
    """
        A plugin to extract emojis from text.

    """

    def filter(self, lst, target_key=None):
        """
            Filters emojis from data and return the result in a dictionary with key called 'emojis'.
            Suports emojis with different skin colors tones, flags and ZWJ sequences of emojis.


            :param lst: texts for emoji extraction
            :type lst: list of strings or list of dictionaries
            :param target_key: a valid key that contains the text.
                    if the data parameter is a list of dictionaries, this parameter is mandatory.
            :type target_key: string
            
            :return: data received and emojis extracted
                    dictionary or list of dictionaries, where dictionaries will have a key called 'emojis' with the result
            :rtype dictionary or list of dictionaries
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
                emojis = self.extract_emojis(element)
                result['emojis'] = emojis
            elif list_of_dicts:
                emojis = self.extract_emojis(element[target_key])
                element['emojis'] = emojis
                result = element

            results.append(result)
        if len(results) > 0:
            return results
        else:
            return None

    def extract_emojis(self, text):
        """
            Extract the emoji sequences from the text.
            Support emojis with different skin colors tones, flags and ZWJ sequences of emojis.

        :param text: text to filter emojis, if they exist
        :type text: string
        :return: emoji sequences
        :rtype: list of strings
        """
        if type(text) is not str:
            raise TypeError(f"Parameter 'text' is of type {type(text)}. This parameter must be an instance of string.")
        emoji_sequences = []
        list_words = text.split()

        # regex for flags
        flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]+', text)
        for word in list_words:
            if any(char in emoji.UNICODE_EMOJI for char in word):
                # clears characters that are neither emoji nor codepoint for skintone
                # ("Emoji Modifier Fitzpatrick Type-1-2") and neither "Zero Width Joiner" character
                only_emojis = ''.join([c if c in emoji.UNICODE_EMOJI or unicodedata.name(c).startswith(
                    "EMOJI MODIFIER") or unicodedata.name(c) == 'ZERO WIDTH JOINER' else ' '
                                       for c in word])
                list_emojis = only_emojis.split()
                emoji_sequences += list_emojis
        return emoji_sequences + flags


