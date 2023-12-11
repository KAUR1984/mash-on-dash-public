from workflow_manager.job_creator import JobCreator
from workflow_manager.flow_creator import FlowCreator
from workflow_manager.workflow_creator import WorkflowCreator
from plugins.enum.plugins_enum import PluginsEnum
from plugins.utils.tokens_keys import TWITTER_TOKENS


# from plugins.file_utils_plugin import FileUtilsPlugin


def execute_workflow_1():
    conf_job1 = {'method_name': 'configure',
                 'args': [TWITTER_TOKENS]}

    conf_job2 = {'method_name': 'authenticate',
                 'args': [],
                 'input_expected': False}

    conf_job3 = {'method_name': 'search_tweets',
                 'args': ['#Eleições2018', 15, False],
                 'input_expected': False}

    conf_job4 = {'method_name': 'export_csv',
                 'args': ['result']}

    twitter_plugin = JobCreator(plugin=PluginsEnum.TwitterPlugin)
    job1 = twitter_plugin.create_job(conf_job1)
    job2 = twitter_plugin.create_job(conf_job2)
    job3 = twitter_plugin.create_job(conf_job3)

    csv_plugin = JobCreator(plugin=PluginsEnum.CsvPlugin)
    job4 = csv_plugin.create_job(conf_job4)

    flow1 = FlowCreator(inputs=[job1], callbacks=[job2]).create_flow()
    flow2 = FlowCreator(inputs=[job3], callbacks=[job4]).create_flow()

    WorkflowCreator(flows=[flow1, flow2]).execute_workflow()


def visualization_workflow():
    conf = {'method_name': 'get_histogram',
            'args': [], 'input_expected': False}

    visualization_plugin = JobCreator(plugin=PluginsEnum.VisualizationPlugin)
    job = visualization_plugin.create_job(conf)
    flow = FlowCreator(inputs=[job]).create_flow()
    WorkflowCreator(flows=[flow]).execute_workflow()


# def execute_workflow_2(folder_name):
#     csv_plugin = JobCreator(plugin=PluginsEnum.CsvPlugin)
#     twitter_plugin = JobCreator(plugin=PluginsEnum.TwitterPlugin)
#     emoji_plugin = JobCreator(plugin=PluginsEnum.EmojiFilterPlugin)
#     ngram_plugin = JobCreator(plugin=PluginsEnum.NGramPlugin)
#     converter_plugin = JobCreator(plugin=PluginsEnum.ConverterPlugin)
#
#     files_names = FileUtilsPlugin().get_path_files('\\Users\\\willi\\\Documents\\SMM Emojis\\' + folder_name + '\\',
#                                                    'csv')
#
#     twitter_config = {'method_name': 'configure',
#                       'args': [TWITTER_TOKENS]}
#     j1 = twitter_plugin.create_job(twitter_config)
#
#     twitter_auth = {'method_name': 'authenticate',
#                     'args': [],
#                     'input_expected': False}
#     j2 = twitter_plugin.create_job(twitter_auth)
#
#     get_tweets_by_ids = {'method_name': 'get_tweets_by_ids',
#                          'args': []
#                          }
#     j4 = twitter_plugin.create_job(get_tweets_by_ids)
#
#     get_emojis = {'method_name': 'filter',
#                   'args': ['full_text']
#                   }
#     j5 = emoji_plugin.create_job(get_emojis)
#
#     n_gram_frequences = {'method_name': 'extract_ngram_frequencies',
#                          'args': [1]
#                          }
#     j6 = ngram_plugin.create_job(n_gram_frequences)
#
#     export_csv = {'method_name': 'export_csv',
#                   'args': []
#                   }
#     j7 = csv_plugin.create_job(export_csv)
#
#     converter_1 = {'method_name': 'merge_lists_of_str_to_str',
#                    'args': []}
#     converter_2 = {'method_name': 'merge_list_of_strs',
#                    'args': []}
#     converter_3 = {'method_name': 'convert_list_of_lists_to_list_of_dicts',
#                    'args': ['frequence']}
#     j8 = converter_plugin.create_job(converter_1)
#     j9 = converter_plugin.create_job(converter_2)
#     j10 = converter_plugin.create_job(converter_3)
#
#     flow_twitter_auth = FlowCreator(jobs=[j1], callback_jobs=[j2]).create_flow()
#     flow_get_emojis = FlowCreator(jobs=[j5], callback_jobs=[j8]).create_flow()
#     flow_export_csv = FlowCreator(jobs=[j7], callback_jobs=[]).create_flow()
#
#     workflow_ls = []
#
#     WorkflowCreator(flows=[flow_twitter_auth]).execute_workflow()
#     for file_name in files_names:
#         import_tweets_ids = {'method_name': 'reading_csv_to_list',
#                              'args': [file_name, 'id'],
#                              'input_expected': False}
#         j3 = csv_plugin.create_job(import_tweets_ids)
#         flow_get_tweet_ids = FlowCreator(jobs=[j3], callback_jobs=[j4]).create_flow()
#         workflow_ls.append(WorkflowCreator(flows=[flow_get_tweet_ids, flow_get_emojis]).get_workflow())
#
#     flow_join_emoji_results = FlowCreator(jobs=workflow_ls, callback_jobs=[j9]).create_flow()
#     flow_get_frequences = FlowCreator(jobs=[j6], callback_jobs=[j10]).create_flow()
#
#     return WorkflowCreator(flows=[flow_join_emoji_results, flow_get_frequences, flow_export_csv]).execute_workflow()


# def execute_workflow_3():
#     csv_plugin = JobCreator(plugin=PluginsEnum.CsvPlugin)
#     twitter_plugin = JobCreator(plugin=PluginsEnum.TwitterPlugin)
#     emoji_plugin = JobCreator(plugin=PluginsEnum.EmojiFilterPlugin)
#     ngram_plugin = JobCreator(plugin=PluginsEnum.NGramPlugin)
#     converter_plugin = JobCreator(plugin=PluginsEnum.ConverterPlugin)
#     filterdata_plugin = JobCreator(plugin=PluginsEnum.FilterDataPlugin)
#
#     files_names = FileUtilsPlugin().get_path_files('\\Users\\\willi\\\Documents\\SMM Emojis\\Hawking Twitter\\', 'csv')
#
#     # AUTENTICAÇÃO DO TWITTER
#     twitter_config = {'method_name': 'configure',
#                       'args': [TWITTER_TOKENS]}
#     twitter_auth = {'method_name': 'authenticate',
#                     'args': [],
#                     'input_expected': False}
#     j_twitter_auth1 = twitter_plugin.create_job(conf=twitter_config)
#     j_twitter_auth2 = twitter_plugin.create_job(conf=twitter_auth)
#
#     # WORKFLOW 1 - EXTRAÇÃO DE EMOJIS DOS TEXTOS DOS TWEETS NÃO TRUNCADOS (SEM RTs)
#     filter_data_1 = {'method_name': 'filter_list_of_dicts',
#                      'args': [{'text': None, 'truncated': 'FALSE', 'id': None, 'isRetweet': 'FALSE'}]}
#     j_filter_1 = filterdata_plugin.create_job(conf=filter_data_1)
#
#     filter_emojis = {'method_name': 'filter',
#                      'args': ['text']
#                      }
#     j_filter_emojis = emoji_plugin.create_job(conf=filter_emojis)
#
#     converter_str1 = {'method_name': 'join_list_of_lists_to_str',
#                       'args': []}
#     j_results_str = converter_plugin.create_job(conf=converter_str1)
#
#     # WORKFLOW 2 - EXTRAÇÃO DE EMOJIS DOS TEXTOS DOS TWEETS TRUNCADOS (SEM RTs) - USO DA API
#     # pega apenas os 'truncated' que não são rt, para pegar o texto inteiro
#     filter_data_2 = {'method_name': 'filter_list_of_dicts',
#                      'args': [{'truncated': 'TRUE', 'id': None, 'isRetweet': 'FALSE'}]}
#     j_filter_2 = filterdata_plugin.create_job(conf=filter_data_2)
#
#     filter_data_3 = {'method_name': 'filter_list_of_dict_to_list',
#                      'args': ['id']}
#     j_filter_3 = filterdata_plugin.create_job(conf=filter_data_3)
#
#     get_tweets = {'method_name': 'get_tweets_by_ids',
#                   'args': []}
#     j_get_tweets = twitter_plugin.create_job(conf=get_tweets)
#
#     aggregate_results = {'method_name': 'join_list_to_str',
#                          'args': []}
#     j_aggregate_results = converter_plugin.create_job(conf=aggregate_results)
#
#     n_gram_frequences = {'method_name': 'extract_ngram_frequencies',
#                          'args': [1]
#                          }
#     j_ngram = ngram_plugin.create_job(conf=n_gram_frequences)
#
#     prepare_csv = {'method_name': 'list_of_lists_to_dict',
#                    'args': ['frequence']}
#     j_prepare_csv = converter_plugin.create_job(conf=prepare_csv)
#
#     export_csv = {'method_name': 'export_csv',
#                   'args': []
#                   }
#     j_export_result = csv_plugin.create_job(export_csv)
#
#     wfs_extract_emojis = []
#
#     # flow de autenticacao do twitter
#     f_twitter_auth = FlowCreator(jobs=[j_twitter_auth1], callback_jobs=[j_twitter_auth2]).create_flow()
#
#     # flow de subworkflows
#     f_filter_tweets_1 = FlowCreator(jobs=[j_filter_1]).create_flow()
#     f_filter_tweets_2 = FlowCreator(jobs=[j_filter_2], callback_jobs=[j_filter_3]).create_flow()
#     f_get_tweets = FlowCreator(jobs=[j_get_tweets]).create_flow()
#
#     # flow comum aos dois subworkflows
#     f_filter_converter_emojis = FlowCreator(jobs=[j_filter_emojis], callback_jobs=[j_results_str]).create_flow()
#
#     f_process_ngrams = FlowCreator(jobs=[j_ngram], callback_jobs=[j_prepare_csv]).create_flow()
#     f_export_csv = FlowCreator(jobs=[j_export_result]).create_flow()
#
#     WorkflowCreator(flows=[f_twitter_auth]).execute_workflow()
#     # Preparando workflows
#     wf_not_truncated = WorkflowCreator(flows=[f_filter_tweets_1, f_filter_converter_emojis]).get_workflow()
#     wf_truncated = WorkflowCreator(flows=[f_filter_tweets_2, f_get_tweets, f_filter_converter_emojis]).get_workflow()
#     for file_name in files_names:
#         read_csv = {'method_name': 'reading_csv_to_list',
#                     'args': [file_name],
#                     'input_expected': False}
#         j_read_csv = csv_plugin.create_job(read_csv)
#         flow_read_csv = FlowCreator(jobs=[j_read_csv], callback_jobs=[wf_not_truncated, wf_truncated]).create_flow()
#         wfs_extract_emojis.append(WorkflowCreator(flows=[flow_read_csv]).get_workflow())
#
#     f_emojis_results = FlowCreator(jobs=wfs_extract_emojis, callback_jobs=[j_aggregate_results]).create_flow()
#     return WorkflowCreator(flows=[f_emojis_results, f_process_ngrams]).execute_workflow()
#     # WorkflowCreator(flows=[f_emojis_results, f_process_ngrams, f_export_csv]).execute_workflow()


# def execute_workflow_4():
#     queries = ['site:oglobo.globo.com bolsonaro']
#     bing_plugin = JobCreator(plugin=PluginsEnum.BingPlugin)
#     filter_data_plugin = JobCreator(plugin=PluginsEnum.FilterDataPlugin)
#     converter_plugin = JobCreator(plugin=PluginsEnum.ConverterPlugin)
#     stopwords_plugin = JobCreator(plugin=PluginsEnum.StopwordsPlugin)
#
#     search_results = {'method_name': 'get_search_results',
#                       'args': ['site:oglobo.globo.com bolsonaro', 'pt-BR', 20]}
#     job_bing = bing_plugin.create_job(conf=search_results)
#
#     filter_data_conf = {'method_name': 'filter_list_of_dict_to_list',
#                         'args': ['snippet']}
#     job_filter = filter_data_plugin.create_job(conf=filter_data_conf)
#
#     converter_conf = {'method_name': 'join_list_to_str',
#                       'args': []}
#     job_converter = converter_plugin.create_job(conf=converter_conf)
#
#     stopwords_conf = {'method_name': '',
#                       'args': []}
#
#     FlowCreator(jobs=[job_bing], callback_jobs=[job_filter])
#     FlowCreator(jobs=[job_converter], callback_jobs=[])


def workflow_get_tweets():
    JobCreator(plugin=PluginsEnum.CsvPlugin)
    JobCreator(plugin=PluginsEnum.FilterDataPlugin)
    JobCreator(plugin=PluginsEnum.ConverterPlugin)

# execute_workflow_2('Hawking Twitter')
# execute_workflow_1()
