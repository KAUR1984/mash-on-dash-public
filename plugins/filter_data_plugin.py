from plugins.filter_plugin import FilterPlugin


class FilterDataPlugin(FilterPlugin):
    """
        A plugin for filtering structured data.

    """

    _key_value = None                      # TODO should be _keys_values?

    def configure(self, keys_values):
        """
            Configures key and values for doing filtering
        :param keys_values: keys and values by which dictionaries will be filtered.
        :type   keys_values: dict
        """
        self._keys_value = keys_values

    def filter(self, data):
        """

        :param data:
        :return:
        """
        if type(data) is list:
            self.filter_list_of_dicts(data, self._keys_values)
        elif type(data) is dict:
            self.filter_dict(data, self._keys_values)
        else:
            raise TypeError(f"Parameter 'data' is of type {type(data)}, must be of type list or list of dicts")

    def filter_list_of_dicts(self, lst_dict, keys_values):
        """
            Filter list of dictionaries by keys and values TODO deleted a copy of this method below.

            :param lst_dict: list of dictionaries to be filtered
            :type lst_dict: list of dictionaries
            :param keys_values: keys and values by which dictionaries will be filtered.
                If the value of any of the keys is None, the function will only filter by the key.
            :type keys_values: dictionary

            :return: a list of filtered dictionaries
            :rtype: list of dictionaries

            Example:
                lst_dicts = [{'name': 'carlos', 'age': 23},
                            {'name': 'ana', 'age': 19}
                            {'name': 'edu', 'age': 19}]
                keys_values = {'name': None, 'age': 19}
                output: [{'name': 'ana', 'age': 19}
                            {'name': 'edu', 'age': 19}]
        """
        if type(lst_dict) is not list:
            raise TypeError(f"Parameter 'ls_dict' is of type {type(lst_dict)}. Must be type of list.")
        if type(keys_values) is not dict:
            raise TypeError(f"Parameter 'dictionary' is of type {type(keys_values)}. Must be type of dict.")
        if not all(isinstance(e, dict) for e in lst_dict):
            raise TypeError(f"All elements of 'ls_dict' must be type of dict.")
        result = []
        for dictionary in lst_dict:
            filtered_dict = self.filter_dict(dictionary, keys_values)
            if filtered_dict:
                result.append(filtered_dict)

        return result

    def filter_dict(self, dictionary, keys_values):
        """
            Filters a dictionary through another dictionary with specified values for each key.
            If the value of any of the keys is None, the function will filter only by the key.

        :param dictionary: dictionary whose keys and values will be filtered.
        :type dictionary: dictionary
        :param keys_values: keys and values by which dictionaries will be filtered.
                If the value of any of the keys is None, the function will only filter by the key.

        :return filtered dictionary
        :rtype dictionary
        """
        if dictionary and keys_values:
            if type(dictionary) is not dict:
                raise TypeError(f"Parameter 'dictionary' is of type {type(dictionary)}. Must be type of dict.")
            if type(keys_values) is not dict:
                raise TypeError(f"Parameter 'dictionary' is of type {type(keys_values)}. Must be type of dict.")
            result = {}

            dict_keys = list(dictionary.keys())
            keys = list(keys_values.keys())
            wrong_keys = [elem for elem in keys if elem not in dict_keys]
            if wrong_keys:
                raise TypeError(f"Some keys doesn't exist in this dictionary: {wrong_keys}")

            filter = True
            for k, v in keys_values.items():
                if v and dictionary[k] == v:
                    result[k] = v
                elif v and dictionary[k] != v:
                    filter = False
                    break
                else:
                    result[k] = dictionary[k]
            if not filter:
                return {}
            return result
