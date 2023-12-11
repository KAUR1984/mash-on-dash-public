from workflow_manager.job_creator import JobCreator
from workflow_manager.flow_creator import FlowCreator
from workflow_manager.workflow_creator import WorkflowCreator
from plugins.enum.plugins_enum import PluginsEnum
import glob
from plugins.utils.tokens_keys import TWITTER_TOKENS


def workflow_most_common_emojis(folder_name):
    csv_plugin = JobCreator(plugin=PluginsEnum.CsvPlugin)
    twitter_plugin = JobCreator(plugin=PluginsEnum.TwitterPlugin)
    emoji_plugin = JobCreator(plugin=PluginsEnum.EmojiFilterPlugin)
    ngram_plugin = JobCreator(plugin=PluginsEnum.NGramPlugin)
    converter_plugin = JobCreator(plugin=PluginsEnum.ConverterPlugin)

    files_names = glob.glob('\\Users\\\willi\\\Documents\\SMM Emojis\\' + folder_name + '\\**\\*.csv', recursive=True)     #TODO this address is not valid.

    job_conf_twitter = twitter_plugin.create_job(conf={'method_name': 'configure',
                                                       'args': [TWITTER_TOKENS]})

    job_auth_twitter = twitter_plugin.create_job(conf={'method_name': 'authenticate',
                                                       'args': [],
                                                       'input_expected': False})

    job_get_tweets = twitter_plugin.create_job(conf={'method_name': 'get_tweets_by_ids',
                                                     'args': []
                                                     })

    print("Printing job_get_tweets" + str(job_get_tweets))

    job_emojis = emoji_plugin.create_job(conf={'method_name': 'filter',
                                               'args': ['full_text']
                                               })

    print("Printing job_emojis" + str(job_emojis))

    job_ngram = ngram_plugin.create_job(conf={'method_name': 'extract_ngram_frequencies',
                                              'args': [1]
                                              })

    print("Printing job_ngram" + str(job_ngram))

    job_export_csv = csv_plugin.create_job(conf={'method_name': 'export_dict_to_csv',
                                                 'args': []
                                                 })

    job_join_emoji_results = converter_plugin.create_job(conf={'method_name': 'merge_lists_of_str_to_str',
                                                               'args': []})
    job_merge_results = converter_plugin.create_job(conf={'method_name': 'merge_list_of_strs',
                                                          'args': []})
    job_prepare_csv = converter_plugin.create_job(conf={'method_name': 'convert_list_of_lists_to_list_of_dicts',
                                                        'args': ['frequence']})

    job_filter_dict_emoji = converter_plugin.create_job(conf={'method_name': 'convert_list_of_dicts_to_list',
                                                              'args': ['emojis']})

    flow_twitter_auth = FlowCreator(input_workpiece=[job_conf_twitter],
                                    output_workpiece=[job_auth_twitter]).create_flow()
    flow_get_emojis = FlowCreator(input_workpiece=[job_emojis], output_workpiece=[job_filter_dict_emoji]).create_flow()
    flow_merge_emoji_results = FlowCreator(input_workpiece=[job_join_emoji_results], output_workpiece=[]).create_flow()
    flow_export_csv = FlowCreator(input_workpiece=[job_export_csv], output_workpiece=[]).create_flow()

    workflow_ls = []

    WorkflowCreator(flows=[flow_twitter_auth]).execute_workflow()
    for file_name in files_names:
        job_read_ids = csv_plugin.create_job(conf={'method_name': 'reading_csv_to_list',
                                                   'args': [file_name, 'id'],
                                                   'input_expected': False})
        flow_get_tweet_ids = FlowCreator(input_workpiece=[job_read_ids],
                                         output_workpiece=[job_get_tweets]).create_flow()
        workflow_ls.append(
            WorkflowCreator(flows=[flow_get_tweet_ids, flow_get_emojis, flow_merge_emoji_results]).get_workflow())

        print("printing workflow_ls" + workflow_ls)

    flow_join_all_emoji_results = FlowCreator(input_workpiece=workflow_ls,
                                              output_workpiece=[job_merge_results]).create_flow()
    flow_get_frequences = FlowCreator(input_workpiece=[job_ngram], output_workpiece=[job_prepare_csv]).create_flow()

    return WorkflowCreator(flows=[flow_join_all_emoji_results, flow_get_frequences, flow_export_csv]).execute_workflow()
