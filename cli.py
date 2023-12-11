from server import create_web_server, add_new_plugins
import sys

""" Cli interface for starting app """

# Command for start redis service:
#               sudo service redis-server start OR brew services start redis (on Mac)
# Command for start celery worker:
#               celery -A workflow_manager.celery_worker.celery worker --loglevel=info -P eventlet
# Command for delete all messages from worker:
#               celery -A workflow_manager.celery_worker.celery purge -f
# Command for start web application:
#               python cli.py

if __name__ == "__main__":
    lst_args = sys.argv[1:]
    dict_args = dict([arg.split('=') for arg in lst_args])
    if 'add_plugins' in dict_args:
        new_plugins = dict_args['add_plugins'].split(',')
        add_new_plugins(new_plugins)

    app = create_web_server()
    app.run(port='5000', debug=True)
