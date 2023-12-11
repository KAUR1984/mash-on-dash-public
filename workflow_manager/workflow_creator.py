from celery import chain


class WorkflowCreator(object):
    """
        Creates an executable workflow, which joins flows.

    """
    _workflow = None

    def __init__(self, flows=None):
        """
            It receives a workpieces parameter that is a list of flows or workflows,
            and chains them in the order they appear in the list.

        :param flows: a list with flows and workflows
        :type flows: list
        """
        if not flows:
            raise TypeError("Parameter 'flows' is required.")
        if type(flows) is not list:
            raise TypeError("Parameter 'flows' must be a instance of list.")

        len_flows = len(flows)
        if len_flows == 1:
            self._workflow = flows[0]
        elif len_flows > 1:
            self._workflow = chain(flows)

    def get_workflow(self):
        """
            Returns the workflow created.

        :return: workflow
        :rtype: chain
        """
        if not self._workflow:
            raise NotImplementedError("Please, call 'create_workflow' before.")
        return self._workflow

    def execute_workflow(self):
        """
            Executes the workflow

        :return: an object that represents the result of the workflow
        :rtype: AsyncResult
        """
        if not self._workflow:
            raise NotImplementedError("Please, call 'create_workflow' before.")
        return self._workflow.apply_async()
