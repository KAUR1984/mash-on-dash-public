from workflow_manager.plugin import Plugin
import csv
import codecs
import time


class CsvPlugin(Plugin):
    """ A plugin that handles csv files to extract or export data.

    """

    def export_dict_to_csv(self, lst_dicts, folder=None, file_name=None, encoding='utf-8-sig'):
        """
            Writes data from a dictionary to a csv file

            :param lst_dicts: dictionaries that will be exported. mandatory.
            :type lst_dicts: list of dictionaries
            :param folder: string that contains the complete path to save the csv file
                default: will save the csv file in current directory
            :type folder: str
            :param file_name: name of the csv file that will be generated
                default is 'result-YY-MMM-DD HhMmSs'
            :type file_name: str
            :param encoding: enconding for csv file
                full list of encodings: https://docs.python.org/3/library/codecs.html#standard-encodings
                default is 'utf-8-sig'
            :type encoding: str

        """

        if not type(lst_dicts) is list:
            raise TypeError(f"Parameter 'lst_dicts' is an instance of {type(lst_dicts)}, must be an instance list.")
        if len(lst_dicts) > 0:
            valid_element_types = all(isinstance(d, dict) for d in lst_dicts)
            if not valid_element_types:
                raise TypeError(f"All elements inside of parameter 'lst_dicts' must be instance of a dict.")
        else:
            raise ValueError(f"Parameter 'lst_dicts' is empty.")
        if not file_name:
            moment = time.strftime('%Y-%m-%d %Hh%Mm%Ss')
            file_name = f"result-{moment}"
        if not folder:
            file_path = f"{file_name}.csv"
        else:
            file_path = f"{folder}\\{file_name}.csv"
        if lst_dicts:
            fieldnames = sorted(list(set(k for d in lst_dicts for k in d)))
            with open(file_path, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                try:
                    writer.writerows(lst_dicts)
                except csv.Error as e:
                    raise Exception(f"An error ocurred writing the csv file", e)

    def reading_csv_to_list(self, file_path, filter_by_columns=None):
        """ Reads data from a csv file and returns it in a list

            :param file_path: complete file path for the csv file. mandatory.
            :type file_path: string
            :param filter_by_columns: reads only the specified columns. default is none.
            :type filter_by_columns: list or strings

            :return: data read from csv file
            :rtype list of strings or list of dictionaries
            """
        if not type(file_path) is str:
            raise TypeError(
                f"Parameter 'file_path' is of type {type(file_path)}. This attribute must be an instance of string.")
        if not file_path.lower().endswith('.csv'):
            raise ValueError(f"Parameter 'file_path' must be pointing to a file with csv extension.")
        result = []
        with codecs.open(file_path, encoding="utf-8", errors='ignore') as f:
            records = csv.DictReader(f)
            for row in records:
                dict_row = dict(row)
                if filter_by_columns:
                    if type(filter_by_columns) is list:
                        dict_filtered = {}
                        for column in filter_by_columns:
                            dict_filtered.insert({column: dict_row['column']})
                        result.append(dict_filtered)
                    elif type(filter_by_columns) is str:
                        result.append(dict(row)[filter_by_columns])
                else:
                    result.append(dict_row)
        return result
