""" Entrypoint for the Celery worker """

from server import create_celery

celery = create_celery()
