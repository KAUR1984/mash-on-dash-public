from workflow_manager.plugin import Plugin


class ConverterPlugin(Plugin):
    """
        A plugin that handles type conversions, data joins, and other transformations with structured data


    """

    def merge_lists_of_str_to_str(self, list_of_lists):
        """
            Receive a list and each list element is a list of strings.
            Concatenates these strings into a single string and returns it.

        :param list_of_lists: list of lists of string
        :type list_of_lists: list of lists of string

        :return: return None if result is empty or parameter 'list_of_lists' is an empty list
                otherwise, return all strings concatenated in a single string.
        :rtype: string or None
        """
        print(list_of_lists)
        if type(list_of_lists) is not list:
            raise TypeError(f"Parameter 'list_of_lists' received is of type {type(list_of_lists)}. "
                            f"This parameter must be an instance of list. ")
        if not all(isinstance(ls, list) for ls in list_of_lists):
            raise TypeError(f"All elements of parameter 'list_of_lists' must be of type list")
        result = ''
        for ls in list_of_lists:
            result_str = self.merge_list_of_strs(ls)
            if result_str:
                result += result_str
        if not result.strip():
            return None
        else:
            return result

    def merge_list_of_strs(self, lst):
        """
            Receive a list and each element is a string.
            Concatenates these strings into a single string and returns it

        :param lst: list contains strings which will be concatenated
        :type lst: list of strings

        :return: a join of all strings in the list
        :rtype: string
        """
        if type(lst) is not list:
            raise TypeError(f"Parameter 'lst' received is of type {type(lst)}. "
                            f"This parameter must be an instance of list. ")

        if all(isinstance(e, str) for e in lst):
            result = ''
            result += ' '.join(lst)
            result += ' '
        else:
            raise TypeError("All elements inside nested lists of parameter 'lst' must be of type string")

        if not result.strip():
            return None
        else:
            return result

    def convert_list_of_lists_to_list_of_dicts(self, lst_of_lst, key_name):
        """
            Given a list of lists, for each nested list, creates a new dictionary where the list
            will be the value for a given key. Returns a list of all these dictionaries.

        :param lst_of_lst: list of lists to convert in a list of dicts
        :type lst_of_lst: list of lists
        :param key_name: key name for resulting dictionary, which will contain the lists as value
        :type key_name: string

        :return list of dictionaries, where each dictionary has a key passed as
                parameter on 'key_name', and as value a list
        :rtype: list of dictionaries
        """
        if type(lst_of_lst) is not list:
            raise TypeError(f"Parameter 'lst_of_lst' received is of type {type(lst_of_lst)}. "
                            f"This parameter must be an instance of list. ")
        if not all(isinstance(lst, list) for lst in lst_of_lst):
            raise TypeError("All elements inside of parameter 'lst_of_lst' must be of type list")
        if type(key_name) is not str:
            raise TypeError(f"Parameter 'key_name' received is of type {type(key_name)}. "
                            f"This parameter must be an instance of string. ")
        results = []
        for lst in lst_of_lst:
            result = {}
            result[key_name] = lst
            results.append(result)
        return results

    def merge_list_of_lists(self, lst_of_lst):
        """
            Merge nested lists into a single list

        :param lst_of_lst: list containing other lists that will be merge
        :rtype lst_of_lst: list of lists

        :return: merged lists
        :rtype list
        """

        if type(lst_of_lst) is not list:
            raise TypeError(f"Parameter 'lst_of_lst' received is of type {type(lst_of_lst)}. "
                            f"This parameter must be an instance of list. ")
        if not all(isinstance(lst, list) for lst in lst_of_lst):
            raise TypeError("All elements inside of parameter 'lst_of_lst' must be of type list")

        result = []
        for ls in lst_of_lst:
            result += ls
        return result

    def convert_list_of_dicts_to_list(self, ls_dict, key):
        """
            Extracts from a list of dictionaries only the values of a given key and returns a list with those values.

            :param ls_dict: list of dictionaries where will be extracted values for specific keys
            :type ls_dict: list
            :param key: key for extract values from dictionaries
            :type key: string

            :return list of values from dictionaries of given key
            :rtype list
        """
        if type(ls_dict) is not list:
            raise TypeError(f"Parameter 'dictionary' is of type {type(ls_dict)}. Must be type of list.")
        if type(key) is not str:
            raise TypeError(f"Parameter 'dictionary' is of type {type(key)}. Must be type of str.")
        result = []
        for dictionary in ls_dict:
            if type(dictionary) is not dict:
                raise TypeError(
                    f"Elements inside parameter 'dictionary' is of type {type(dictionary)}. Must be type of dict.")
            if key in dictionary:
                result.append(dictionary[key])
            else:
                raise TypeError(f"Key '{key}' is not present in dictionaries")
        return result
