from celery import group, chain, chord
from workflow_manager import celery


class FlowCreator(object):
    """
        Creates a flow which joins one or more workpieces (job or workflows)

    """
    _input_workpieces = None
    _output_workpiece = None

    def __init__(self, input_workpiece=None, output_workpiece=None):
        """
            Initialize a flow with input and output workpieces.

        :param input_workpiece: jobs or workflows that are executing in parallel.
            This parameter is mandatory and must have at least one element.
        :type input_workpiece: list
        :param output_workpiece: jobs or workflows that executing in parallel, after execution of input workpieces
        :type output_workpiece: list or None
        """
        if type(input_workpiece) is not list:
            raise TypeError("Parameter 'input_workpiece' must be a instance of list.")
        if len(input_workpiece) == 0:
            raise TypeError("Parameter 'input_workpiece' is a list and must have elements.")
        if not output_workpiece:
            output_workpiece = []

        self._input_workpieces = input_workpiece
        self._output_workpiece = output_workpiece

    def create_flow(self):
        """
            Creates a flow.

        :return: flow created
        :rtype: a chain, chord or group
        """
        flow = None

        length_inputs = len(self._input_workpieces)
        length_callbacks = len(self._output_workpiece)

        flow_1 = True if length_inputs == 1 and length_callbacks == 0 else False
        flow_2 = True if length_inputs >= 1 and length_callbacks == 0 else False
        flow_3 = True if length_inputs >= 1 and length_callbacks == 1 else False
        flow_4 = True if length_inputs == 1 and length_callbacks == 1 else False

        if flow_1:
            flow = self._input_workpieces[0]
        elif flow_2:
            flow = group(self._input_workpieces, app=celery)
        elif flow_3:
            group_input = group(self._input_workpieces, app=celery)
            flow = chord(header=group_input, body=self._output_workpiece[0], app=celery)
        elif flow_4:
            flow = chain(self._input_workpieces[0], self._output_workpiece[0])

        return flow
