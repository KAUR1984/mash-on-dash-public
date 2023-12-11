import plugins as plugins
import pkgutil
import importlib

from plugins.api_plugin import ApiPlugin
import plugins.bing_plugin

"""
    This module is dedicated to united all utilities for this project.
"""


def camel_case_to_joined_lower(string):
    """
        Receives a string in CamelCase and returns it in joined_lower
    :param string: string in camel case
    :type string: string
    :return: string in joined lower
    :rtype: string
    """
    to_joined_lower = ('_' + char if char.isupper() and i != 0 else char for i, char in enumerate(string))
    return ''.join(to_joined_lower).lower()


def joined_lower_to_camel_case(string):
    """
        Receives a string in joined_lower and returns it in CamelCase
    :param string: string in joined lower
    :type string
    :return string in camel case
    :rtype string
    """
    return ''.join([w.title() for w in string.split('_')])


def joined_lower_to_spaced(string):
    """
        Convert the module name from joined lower to separated by space.
    :param string: string in joined lower
    :type: string
    :return: string separated by space
    :rtype: string
    """
    return ''.join( w + " " for w in string.split('_'))


def spaced_to_joined_lower(string):
    """
        Convert the module name from spaced string to joined_lower
    :param string: spaced string
    :type: string
    :return: joined_lower string
    :rtype: string
    """
    return ''.join(w.lower() + "_" for w in string.split(' '))


def get_plugins_modules():
    """
        In the plugins folder, search for all plugins models
    :return: list of plugins models
    :rtype: list of strings
    """
    base_package = plugins.__name__
    print("Printing base_package which is plugins.__name__ : " + base_package)        # TODO remove the print
    plugin_modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
        if not ispkg:
            plugin_modules.append("{}.{}".format(base_package, modname))
    return plugin_modules


def find_api_plugin_modules():
    """
        In the plugins folder, search for all API plugins based on 2 categories:
        1. Extends the API_plugin class
        2. Not an abstract class
        TODO might need to generalise this method to arbitrary abstract classes.

    :return: list of API plugins models
    :rtype: list of strings
    """
    base_package = plugins.__name__
    api_plugin_modules = []

    # import_all_plugins()

    for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):

        if not ispkg:
            plugin_ = __str_to_class(joined_lower_to_camel_case(modname))
            is_abstract = bool(getattr(plugin_, "__abstractmethods__", False))

            if issubclass(plugin_, ApiPlugin):  # and (not is_abstract):

                print("modname: " +
                      str(modname) +
                      " ; Plugin class: " +
                      str(__str_to_class(joined_lower_to_camel_case(modname))) +
                      " is a subclass of ApiPlugin: " +
                      str(issubclass(__str_to_class(joined_lower_to_camel_case(modname)), ApiPlugin)))

                api_plugin_modules.append("{}".format(modname))
                print("Adding to the API modules list: {}.{}".format(base_package, modname))

    print("Printing API modules: " + str(api_plugin_modules))
    return api_plugin_modules


def get_module_name_plugin_class_name(class_name):
    """
        Given the name of the plugin class, it takes the name of its module
    :param class_name: class name of the plugin
    :type class_name: string
    :return: module name of the plugin
    :rtype: string
    """
    base_package = plugins.__name__
    plugin_name = camel_case_to_joined_lower(class_name)
    for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
        if not ispkg and plugin_name == modname:
            return f"{base_package}.{modname}"


def get_plugin_class_name_from_module_name(modname):
    """
        Given the name of the plugin module, it returns the name of plugin class.
    :param modname: module name of plugin
    :type modname: string
    :return: class name of plugin
    :rtype: string
    """
    print("Printing modname: " + str(modname))
    plugin_class_name = joined_lower_to_camel_case(modname)
    for importer, module_name, ispkg in pkgutil.iter_modules(plugins.__path__):
        if not ispkg and module_name == modname:
            print("Printing modname and plugin class name: " + str(modname) + " " + str(plugin_class_name))
            return f"{plugin_class_name}"


# def import_all_plugins():
#     """
#         Import the classes in the plugin modules for use globally.
#       TODO : remove this method before handover.
#     """
#     module_name_list = get_plugins_modules()
#
#     for i in range(0, len(module_name_list)):
#         globals()[module_name_list[i]] = importlib.import_module(module_name_list[i])
#
#         print("Printing globals: " + str(globals()[module_name_list[i]]))


def __str_to_class(classname):
    """
        Given the name of a class, it returns the corresponding class object.
        TODO put exception handling here.
    :param classname: class name of the entity
    :type classname: string
    :return: corresponding class object
    :rtype: <class object>
    """

    print("Printing classname: " + str(classname))
    # print("Printing eval(classname): " + str(eval(get_module_name_plugin_class_name(classname) + f".{classname}")))

    module = importlib.import_module(get_module_name_plugin_class_name(classname))
    return getattr(module, classname)
