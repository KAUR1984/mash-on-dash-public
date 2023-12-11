import logging
from server.controller import routes, visualization
from workflow_manager import celery
from config import Config
import importlib
from workflow_manager.plugin import Plugin
from plugins.utils.utils import joined_lower_to_camel_case, get_plugins_modules

""" This module is dedicated to configure Celery with Flask in a factory pattern
    Creates the application factory """

logger = logging.getLogger()

new_plugins = None


def add_new_plugins(lst_new_plugins):
    global new_plugins
    new_plugins = lst_new_plugins


def create_web_server(debug=False):
    return entrypoint(debug=debug, mode='server')


def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')


def entrypoint(debug=False, mode='server'):
    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('server', 'celery'), 'bad mode "{}"'.format(mode)

    server = visualization.server
    server.debug = debug

    configure_server(server)
    configure_logging(debug=debug)
    configure_celery(server, celery)  # CELERY
    register_plugin_tasks(celery)  # CELERY

    # register blueprints
    server.register_blueprint(routes.bp, url_prefix='')

    if mode == 'server':
        return server
    elif mode == 'celery':
        return celery


def configure_server(server):
    logger.info('configuring flask server')
    server.config.from_object(Config)


def configure_celery(server, celery):
    """ Configure celery instance and make all tasks executing
        inside flask application context """

    celery.conf['BROKER_URL'] = server.config['BROKER_URL']
    celery.conf['CELERY_RESULT_BACKEND'] = server.config['CELERY_RESULT_BACKEND']
    celery.conf['CELERY_ACKS_LATE'] = server.config['CELERY_ACKS_LATE']
    celery.conf['CELERYD_CONCURRENCY'] = server.config['CELERYD_CONCURRENCY']
    # celery.conf['CELERY_TASK_RESULT_EXPIRES'] = server.config['CELERY_TASK_RESULT_EXPIRES']
    celery.conf['CELERYD_PREFETCH_MULTIPLIER'] = server.config['CELERYD_PREFETCH_MULTIPLIER']
    celery.conf['BROKER_HEARTBEAT'] = server.config['BROKER_HEARTBEAT']
    celery.conf['CELERY_TASK_ALWAYS_EAGER'] = server.config['CELERY_TASK_ALWAYS_EAGER']

    # CELERY_INCLUDE is a string of all the plugin modules found,
    # hence, we are concatenating the new plugins found into this string.

    if new_plugins:
        celery.conf['CELERY_INCLUDE'] += tuple(new_plugins)

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task

    class AppContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with server.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()


def configure_logging(debug=False):
    root = logging.getLogger()
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(fmt)

    root.addHandler(h)

    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)


def register_plugin_tasks(celery):
    """ Register all plugins as task for celery """
    lst_plugins = get_plugins_modules()
    if new_plugins:
        lst_plugins += new_plugins
    for module_name in lst_plugins:
        plugin_module_name = module_name.split('.')[-1]
        class_name = joined_lower_to_camel_case(plugin_module_name)
        module = importlib.import_module(module_name)
        plugin_ = getattr(module, class_name)
        is_abstract = bool(getattr(plugin_, "__abstractmethods__", False))
        if issubclass(plugin_, Plugin) and not is_abstract:
            celery.register_task(plugin_())
