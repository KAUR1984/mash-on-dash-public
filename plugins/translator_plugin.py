from googletrans import Translator
from workflow_manager.plugin import Plugin


class TranslatorPlugin(Plugin):
    """
        Translates a given text using Google Translate API.

    Attributes:
        _lang: language to translate
        _translator_instance: translator

    """
    _translator_instance = None

    def configure(self):
        """
            Configure the plugin.

        """
        self._translator_instance = Translator()

    def translate(self, text, dest_lang='en', source_lang=None):
        """
            Translates a give

        :param text: text to translate
        :type text: string
        :param dest_lang: the destination language you want to translate
                default is 'en'. valid values: iso639-1 language codes.
                see the list here: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        :type dest_lang: string
        :param source_lang: the source language you want to translate.
                not required. if source language is not given,
                google translate attempts to detect.
        :type source_lang: string


        :return: text translated for destination language
        :rtype: string
        """
        if not self._translator_instance:
            raise RuntimeError(f"Method configure must be called before the usage.")
        if source_lang and type(source_lang) is not str:
            raise TypeError(f"Parameter 'source_lang' is of type {type(source_lang)}, must be of type string.")
        if type(dest_lang) is not str:
            raise TypeError(f"Parameter 'dest_lang' is of type {type(dest_lang)}, must be of type string.")

        if source_lang:
            return self._translator_instance.translate(text, dest=dest_lang, src=source_lang).text
        else:
            return self._translator_instance.translate(text, dest=dest_lang).text
