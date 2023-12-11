from plugins.utils import utils

""" Config for Flask and Celery instance """


class Config:
    SECRET_KEY = 'top-secret!'
    DEBUG = True
    # Celery configs
    BROKER_URL = 'redis://127.0.0.1:6379/'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/'
    CELERYD_CONCURRENCY = 1
    CELERY_ACKS_LATE = True
    # CELERY_TASK_RESULT_EXPIRES = 36000
    CELERYD_PREFETCH_MULTIPLIER = 1
    BROKER_HEARTBEAT = 0
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_INCLUDE = utils.get_plugins_modules()


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
