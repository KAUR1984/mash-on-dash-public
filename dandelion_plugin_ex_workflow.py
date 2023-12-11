from plugins.dandelion_plugin import DandelionPlugin
from plugins.enum.plugins_enum import PluginsEnum
from plugins.utils.private_token_keys import DANDELION_API_KEY_PRIVATE
from workflow_manager.flow_creator import FlowCreator
from workflow_manager.job_creator import JobCreator
from workflow_manager.workflow_creator import WorkflowCreator


def configure_dandelion_json_workflow(input_text):
    print("Printing input text received: " + str(input_text))

    dandelion_plugin = JobCreator(plugin=PluginsEnum.DandelionPlugin)

    job_conf_dandelion = dandelion_plugin.create_job(conf={'method_name': 'configure',
                                                           'args': [DANDELION_API_KEY_PRIVATE]})

    job_get_entities = dandelion_plugin.create_job(conf={'method_name': 'get_entities',
                                                         'args': [input_text]})

    print("printing job get entities: " + str(job_get_entities))

    flow_get_entities = FlowCreator(input_workpiece=[job_conf_dandelion],
                                    output_workpiece=[job_get_entities]).create_flow()

    # Execute the final workflow

    workflow_ls = [WorkflowCreator(flows=[flow_get_entities]).execute_workflow()]

    # call the dandelion plugin class methods manually to get the output list ------------ TODO
    dp = DandelionPlugin()
    dp.configure(api_key=DANDELION_API_KEY_PRIVATE)
    dandelion_result = dp.get_entities(text=input_text)
    print("Printing manual dandelion result: " + str(dandelion_result) + " Type: " + str(type(dandelion_result)))
    # -----------------------------------------------------------------

    print("Printing completed workflow execution: " + str(workflow_ls))
    return dandelion_result

