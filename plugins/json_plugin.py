from workflow_manager.plugin import Plugin
import json
import io
import time


class JsonPlugin(Plugin):
    """
        A plugin that handles json files to extract or export data.

    Attributes:
        _output_json: json file to be exported
        _directory_path: job directory where json files will be read or saved

    """
    _output_json = None
    _directory_path = None

    def configure(self, directory_path):
        """
            Configure the plugin with a desirable directory path

        :param directory_path: path where you want to read or save a json file
        :type: directory_path: string
        """
        if type(directory_path) is not str:                   # I think here it should be `not str` TODO
            raise TypeError(
                f"Parameter 'directory_path' is of type {type(directory_path)}. "
                f"This parameter must be an instance of string.")
        self._directory_path = directory_path

    def export_list_of_dicts_into_json(self, lst_dicts, file_name=None):
        """"
            Write a list of dictionaries into a json file

            :param lst_dicts: list that has data to write to a json file
            :type lst_dicts: list of dictionaries
            :param file_name: file name that will be exported.
                default is 'result-YY-MMM-DD HhMmSs'
            :type file_name: string

            :return a message of success
            :rtype string

        """
        if not self._directory_path:
            raise RuntimeError("There isn't 'directory_path' configured for this plugin. "
                               "Please, call configure before usage.")
        if file_name and type(file_name) is str:                # Should be not ? TODO
            raise TypeError(f"Parameter file_path is instance of {type(file_name)}, must be instance of str.")
        if not type(lst_dicts) is list:
            raise TypeError(f"Parameter lst_dicts is of type {type(lst_dicts)}, must be instance of list.")
        valid_types_lst = all(isinstance(d, dict) for d in lst_dicts)
        if not file_name:
            moment = time.strftime('%Y-%m-%d %Hh%Mm%Ss')
            file_name = f"result-{moment}"
        if not valid_types_lst:
            raise TypeError(f"All elements inside of lst_dicts must be instance of a dict.")
        else:
            self._output_json = io.open(self._directory_path + file_name + '.json', 'a', newline='\n',
                                        encoding='utf-8-sig')
            for d in lst_dicts:
                json.dump(d, self._output_json)
                self._output_json.write('\n')
            self._output_json.close()
            self._output_json = None
            return 'Data successfully exported to a json file'

    def read_json_to_lst_of_dicts(self, file_name):
        """
            Read data from a json file and returns a list of dictionaries

            :param file_name: file name
            :type file_name: string

            :return: structured data read from json file
            :rtype list of dictionaries
        """
        if not self._directory_path:
            raise RuntimeError("There isn't 'directory_path' configured for this plugin. "
                               "Please, call configure before usage.")
        if not file_name and not type(file_name) is str:
            raise TypeError(f"Parameter 'file_name' is instance of {type(file_name)}, must be instance of str.")
        result = []
        with open(self._directory_path + file_name + '.json', 'r', encoding='utf-8-sig') as f:
            for line in f:
                line_content = json.loads(line)
                result.append(line_content)

        return result
