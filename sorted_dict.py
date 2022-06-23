from bisect import insort_right


class SortedDict(object):
    """
    implementation for OrderedDict.
    """
    def __init__(self, by: str = "key", size=1000):
        """
        Args:
            by: str, "key" or "value"
            size: int, size of the hash table
        """
        self.storage = [[] for _ in range(size)]
        self.hash_order = []
        self.by = by
        self.size = size
        self.length = 0
        # if by == "key":
        #     self.key_func = lambda x: x[0]
        # elif by == "value":
        #     self.key_func = lambda x: x[1]

    def __setitem__(self, key, value):
        """
        set key value, if conflict, append to the sub list
        """
        storage_idx = hash(key) % self.size
        for ele in self.storage[storage_idx]:
            if key == ele[0]:  # already exist, update it
                if self.by == "value":
                    alter_idx = self.hash_order.index([storage_idx, ele[1]])
                    self.hash_order[alter_idx][1] = value
                ele[1] = value
                break
        else:
            self.storage[storage_idx].append([key, value])
            hash_value = key if self.by == "key" else value
            insort_right(self.hash_order, [storage_idx, hash_value], key=lambda x: x[1])
            self.length += 1
    
    def __getitem__(self, key):
        """
        get by key, if not found, raise key error
        :raise: KeyError
        :return: value
        """
        storage_idx = hash(key) % self.size
        for ele in self.storage[storage_idx]:
            if ele[0] == key:
                return ele[1]

        raise KeyError('Key {} dont exist'.format(key))

    def __delitem__(self, key):
        """
        delete key value from current dictionary instance
        :param key: str
        :return: None
        """
        storage_idx = hash(key) % self.size
        for sub_lst in self.storage[storage_idx]:
            if key == sub_lst[0]:
                self.storage[storage_idx].remove(sub_lst)
                self.length -= 1
                return

        raise KeyError('Key {} dont exist'.format(key))

    def __contains__(self, key):
        """
        check if key exist in current diction
        :param key: str
        :return: boolean
        """
        storage_idx = hash(key) % self.size
        for item in self.storage[storage_idx]:
            if item[0] == key:
                return True
        return False

    def __len__(self):
        """
        return length
        :return: int
        """
        return self.length

    def __iterate_kv(self):
        """
        return an iterator
        :return: generator
        """
        for sub_lst in self.hash_order:
            yield self.storage[sub_lst[0]][0]

    def __iter__(self):
        """
        return an iterator
        :return: generator
        """
        for key_var in self.__iterate_kv():
            yield key_var[0]

    def keys(self):
        """
        get all keys as list
        :return: list
        """
        return self.__iter__()

    def values(self):
        """
        get all values as list
        :return: list
        """
        for key_var in self.__iterate_kv():
            yield key_var[1]

    def items(self):
        """
        get all k:v as list
        :return: list
        """
        return self.__iterate_kv()

    def get(self, key):
        """
        get value by key
        :param key: str
        :return: value
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def __str__(self):
        """
        str representation of the dictionary
        :return: string
        """
        res = []
        for ele in self.hash_order:
            for key_value in self.storage[ele[0]]:
                if isinstance(key_value[0], str):
                    key_str = '\'{}\''.format(key_value[0])
                else:
                    key_str = '{}'.format(key_value[0])
                if isinstance(key_value[1], str):
                    value_str = '\'{}\''.format(key_value[1])
                else:
                    value_str = '{}'.format(key_value[1])

                res.append('{}: {}'.format(key_str, value_str))

        key_value_pairs_str = '{}'.format(', '.join(res))
        return '{' + key_value_pairs_str + '}'

    def __repr__(self):
        """
        string representation of the class instances
        :return: string
        """
        return self.__str__()
