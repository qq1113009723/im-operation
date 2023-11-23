class DataFilter:
    def __init__(self, primary_data, secondary_data, key_field):
        """
        初始化数据过滤器。

        :param primary_data: 主数据集，将从中过滤掉重复的数据。
        :param secondary_data: 次数据集，用于确定哪些数据是重复的。
        :param key_field: 用于比较数据的关键字段。
        """
        self.primary_data = primary_data
        self.secondary_data = secondary_data
        self.key_field = key_field

    def filter_out_duplicates(self):
        """
        过滤掉主数据集中与次数据集重复的数据。

        :return: 过滤后的数据集。
        """
        secondary_keys = {item[self.key_field] for item in self.secondary_data}
        filtered_data = [item for item in self.primary_data if item[self.key_field] not in secondary_keys]
        return filtered_data
