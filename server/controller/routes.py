import logging
import pdb
from flask import redirect, Blueprint, render_template, request, url_for

from dandelion_plugin_ex_workflow import configure_dandelion_json_workflow
from server.controller import visualization
from smm_workflow import workflow_most_common_emojis
from plugins.utils import utils

"""
    Routes for outputs for front-end are set in this module
"""


bp = Blueprint('pages', __name__)
logger = logging.getLogger()


@bp.route('/', methods=['GET', 'POST'])
def view_base():
    visualization.create_histogram1()
    return render_template('index.html')


@bp.route('/billing')
def view_billing():
    return render_template('other-pages/billing.html')


@bp.route('/my-workflows')
def view_my_workflows():
    pdb.set_trace()
    return render_template('other-pages/my-workflows.html')


@bp.route('/other-pages/create-a-workflow', methods=["GET", "POST"])
def create_a_workflow():
    list_of_entities = []

    if request.method == "POST":

        # getting input with name=getEntities-input-string in HTML form

        print("This post method is being called")
        get_entities_input_string = request.form.get("getEntities-input-string")
        list_of_entities = configure_dandelion_json_workflow(get_entities_input_string)

    # Convert each module name in list to spaced string.

    list_of_api_plugin_modules = [utils.joined_lower_to_spaced(x).title()
                                  for x in utils.find_api_plugin_modules()]

    # Display the list of first 16 plugins on the default processing card

    list_of_default_plugins = [utils.joined_lower_to_spaced(x).title()[8:]
                               for x in utils.get_plugins_modules()]

    total_number_of_plugins = len(list_of_default_plugins)
    number_of_plugins_default = 16
    initial_default_plugins = list_of_default_plugins[:number_of_plugins_default]
    number_of_plugins_left = total_number_of_plugins - number_of_plugins_default

    print("Printing list_of_all_plugin_modules: ")
    print(list_of_api_plugin_modules)

    print("Printing entities: " + str(list_of_entities))

    return render_template('other-pages/create-a-workflow.html',
                           list_api_plugins=list_of_api_plugin_modules,
                           first_eight_list_of_default_plugins=initial_default_plugins[:8],
                           last_eight_list_of_default_plugins=initial_default_plugins[8:],
                           number_of_plugins_left=number_of_plugins_left,
                           list_of_entities=list_of_entities)


@bp.route('/explore-page')
def view_explore_page():
    return render_template('other-pages/explore-page.html')


@bp.route('/help')
def view_help_page():
    return render_template('other-pages/help-page.html')


@bp.route('/contribute')
def view_contribute_page():
    return render_template('other-pages/contribute-page.html')


@bp.route('/notifications')
def view_notifications():
    return render_template('other-pages/notifications.html')


@bp.route('/profile')
def view_profile():
    return render_template('other-pages/profile.html')


@bp.route('/sign-in')
def view_signin():
    return render_template('other-pages/sign-in.html')


@bp.route('/sign-up')
def view_signup():
    return render_template('other-pages/sign-up.html')


@bp.route('/smm')
def execute_smm():
    workflow_most_common_emojis('Chester Twitter')
    return "Executando workflow"


@bp.route('/visual1')
def render_app1():
    visualization.create_histogram1()
    return redirect('/histogram1/')


@bp.route('/visual2')
def render_app2():
    visualization.create_histogram2()
    return redirect('/histogram2/')


@bp.route('/my_page')
def render_my_page():
    visualization.create_histogram1()
    visualization.create_histogram2()
    return render_template('my_template.html')
