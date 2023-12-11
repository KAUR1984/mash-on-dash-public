from enum import Enum


class PluginsEnum(Enum):
    """
        Enum where all existing plugins are listed
    """
    BingPlugin = 1,
    CsvPlugin = 2,
    DandelionPlugin = 3,
    EmojiFilterPlugin = 4,
    FileUtilsPlugin = 5,
    NGramPlugin = 6,
    SentimentAnalysisPlugin = 7,
    StopwordsPlugin = 8,
    TagthewebPlugin = 9,
    TranslatorPlugin = 10,
    TweetCleanerPlugin = 11,
    TwitterPlugin = 12,
    ConverterPlugin = 13,
    FilterDataPlugin = 14,
    DuckDuckGoPlugin = 15