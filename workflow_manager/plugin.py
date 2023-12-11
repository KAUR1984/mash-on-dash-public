from workflow_manager import celery
from celery.utils.log import get_task_logger


class Plugin(celery.Task):
    """
        This class makes a plugin visible and executable for Celery
        and runs a specific method of a plugin, with given arguments.

        If you want create a new plugin, it's mandatory extend this class.

        All plugins must be extends this class.

        This class extends a base class Task from Celery and override the run function,
        where based on arguments and keyword arguments passed for plugin (task),
        can be run specific methods for execution.

    """
    logger = get_task_logger(__name__)
    _expected_exception = Exception
    # home_page_url = ""

    def set_expected_exception(self, exceptions):
        """ This method is for subclass set their expected exceptions when they need

            :param exceptions: expected exceptions
        """
        self._expected_exception = exceptions

    # def get_home_page_url(self):
    #     """
    #         Getter for the url of the home page (if any).
    #
    #     :return: Plugin's website url
    #     :rtype: string
    #     """
    #     return self.home_page_url
    #
    # def set_home_page_url(self, url):
    #     """
    #         Setter for the url of the home page as input by the external user.
    #
    #     """
    #     self.home_page_url = url

    def shadow_name(self, args, kwargs, options):
        return self.__class__.__name__

    def run(self, *args, **kwargs):
        """
            Is the body of the task executed by celery workers.
            It will call a specific method of a plugin with his arguments.

            The run method is called whenever a plugin is actually executed,
            that is, in the execution of a workflow.

        :param args: arguments for an plugin method
        :type args: list
        :param kwargs: keyword arguments that contains the method name that wants to execute
        :type kwargs: dictionary

        :return: the return of execution of plugin method
        """

        if 'method_name' not in kwargs:
            raise RuntimeError(f"Can not execute a plugin method. The keyword argument 'method_name' is required."
                               f"Keyword arguments received: {kwargs.keys()}")
        else:
            try:
                method = getattr(self, kwargs['method_name'])
            except AttributeError as e:
                raise ValueError(f"The 'method_name' wasn't found in {self.__class__.__name__}. ]"
                                 f"The value passed was {kwargs['method_name']}") from e
            # if self.request.chain:
            #     self.logging_next_tasks_in_chain()
            self.logger.info(f"Executing Task: {self.__class__.__name__}.{kwargs['method_name']}")
            kwargs.pop('method_name', None)

            self.logger.info(f"Printing arguments for the method: {str(args)} length : {len(args)}")

            try:
                if len(args) > 1:
                    self.logger.info("Printing method in if statement " + str(method) + "(" + str(args) + ")")
                    return method(args[1])       # was *args before (was giving TypeError exception) hard-coded the index as 1 for dandelion plugin example workflow. Need to change for future implementations TODO
                elif len(args) == 1:
                    return method(args[0])
                else:
                    return method()
            except self._expected_exception as exc:
                raise self.retry(exc=exc)

    def logging_next_tasks_in_chain(self):
        """
            Method to log where the workflow execution step is

        """
        chain = self.request.chain
        kwargs = self.request.kwargs
        list_tasks = []
        if 'method_name' in self.request.kwargs:
            atual_task = f"( {self.__class__.__name__}.{kwargs['method_name']} )"
        if self.request.chain:
            for task in chain:
                task_name = task['task'].split('.')[-1]
                method_name = task['kwargs']['method_name']
                list_tasks.append(f"{task_name}.{method_name}")
            list_tasks.reverse()
            list_tasks.insert(0, atual_task)

        next_tasks_in_chain = ' -> '.join(list_tasks)
        self.logger.info(next_tasks_in_chain)
