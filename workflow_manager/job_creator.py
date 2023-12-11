import importlib
from plugins.enum.plugins_enum import PluginsEnum
from plugins.utils.utils import get_module_name_plugin_class_name
from workflow_manager import celery


class JobCreator(object):
    """
        This class creates the smallest executable part of a workflow, that is,
        the call to execute a plugin method (a signature, for celery).

    """
    conf_required = ('method_name', 'args')
    conf_optional = ('input_expected',)

    _plugin_instance = None

    def __init__(self, plugin=None):
        """ Initializes a JobCreator object with an instance of a plugin.
        This plugin instance is registered in celery.
        This instance is unique for execution, which may vary are your configuration.

        Arguments:
            :param plugin: must be a instance of PluginEnum
            :type plugin: PluginsEnum
        """
        if not (plugin or issubclass(plugin, PluginsEnum)):
            raise TypeError(
                f"Parameter 'plugin' is of type {type(plugin)}. A valid <PluginEnum> instance is expected. ")

        # get an instance of plugin by plugin name

        module_name = get_module_name_plugin_class_name(plugin.name)
        try:
            module = importlib.import_module(module_name)
            plugin_ = getattr(module, plugin.name)
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"An error occurred when tried to get the instance of a plugin.") from e

        self._plugin_instance = celery.register_task(plugin_())

    def create_job(self, conf=None):
        """
            Creates a signature of a plugin from a dictionary of configurations.

        :param conf: a dictionary that represents configurations for create a job.
        :type conf: dictionary

        some configurations are mandatory and will raise an exception if they aren't
        present in dictionary. the required and optional configuration are described below.

        Required configurations:
            key: 'method_name'. value type: str
            description: a string that contains the exact name of the plugin method
            that the user wants to configure the job.

            key: 'args'. value type: list
            description: the arguments of the plugin method.

        Optional configurations:
            key: 'input_expected'. value type: bool
            description: a boolean that indicates whether or not that job depends on a future entry to run.
            Default value is True. If this configuration is not present, the default value is considered.

            Example: { 'method_name': 'add_numbers', 'args': [1,2] }

        :return: a signature for task
        """
        if type(conf) is not dict:
            raise TypeError(
                f"Parameter 'conf' is of {type(conf)}. This parameter is mandatory and must be instance of dict.")
        missing_conf = [conf_required for conf_required in self.conf_required if
                        conf_required not in conf.keys()]
        invalid_conf = [conf for conf in conf.keys() if
                        conf not in self.conf_required and conf not in self.conf_optional]

        if len(invalid_conf) != 0:
            format_keys = ', '.join(invalid_conf)
            raise ValueError(f"Invalid(s) configuration(s) in the 'conf' argument: '{format_keys}'")
        if len(missing_conf) != 0:
            format_keys = ', '.join(missing_conf)
            raise KeyError(f"Missing configuration(s) in the 'conf' argument: '{format_keys}'")

        if type(conf['args']) is not list:
            raise TypeError("Key 'args' of parameter 'conf' must be instance of list")
        if type(conf['method_name']) is not str:
            raise TypeError("Key 'method_name' of parameter 'conf' must be instance of string")

        # if an input is not expected, an immutable signature is used
        if 'input_expected' in conf and not conf['input_expected']:
            return self._plugin_instance.si(*conf['args'], method_name=conf['method_name'])
        else:
            return self._plugin_instance.s(*conf['args'], method_name=conf['method_name'])

