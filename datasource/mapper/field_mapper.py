class FieldMapper:
    def __init__(self):
        # 初始化一个字典来存储每个实体的映射规则
        """
        #这里是一个简化的例子来说明这个结构：
        entity_mapping_rules = {
            'groups': {
                'Type': lambda x: 'public' if x == 1 else 'private' if x == 2 else x,
                # 其他字段映射规则...
            },
            'accounts': {
                # 字段映射规则...
            }
        }
        """
        self.entity_mapping_rules = {}

    def register_mapping(self, entity, field, mapping_func):
        """
        注册一个映射规则。
        :param entity: 要映射的实体类型，例如 'groups' 或 'accounts'。
        :param field: 实体中要映射的字段。
        :param mapping_func: 映射函数，用于转换字段值。
        """
        # 如果实体类型还没有映射规则，初始化一个空字典
        if entity not in self.entity_mapping_rules:
            self.entity_mapping_rules[entity] = {}
        # 为特定字段注册映射函数
        self.entity_mapping_rules[entity][field] = mapping_func

    def map_field(self, entity, field, value):
        """
        映射单个字段。
        :param entity: 实体类型。
        :param field: 要映射的字段。
        :param value: 字段的原始值。
        :return: 映射后的字段值。
        """
        # 获取实体类型的映射规则
        entity_rules = self.entity_mapping_rules.get(entity, {})
        # 如果字段有映射规则，则应用它
        if field in entity_rules:
            return entity_rules[field](value)
        # 如果没有映射规则，返回原始值
        return value

    def map_data(self, data, entity, mapping_config):
        """
        映射数据集中的所有数据。
        :param data: 原始数据集。
        :param entity: 实体类型。
        :param mapping_config: 映射配置。
        :return: 映射后的数据集。
        """
        mapped_data = []
        for item in data:
            mapped_item = {}
            for key, possible_keys in mapping_config.items():
                # 查找原始数据中的值
                value = self.find_value(item, possible_keys)
                # 映射字段值
                mapped_item[key] = self.map_field(entity, key, value)
            mapped_data.append(mapped_item)
        return mapped_data

    @staticmethod
    def find_value(source, keys):
        """
        在数据源中查找给定键列表中的值。
        :param source: 数据源，通常是一个字典。
        :param keys: 键的列表，这些键是可能的数据源字段。
        :return: 找到的值，如果没有找到则返回None。
        """
        for key in keys:
            if key in source:
                return source[key]
        return None


# 使用示例
mapper = FieldMapper()
# 为'groups'实体的'Type'字段注册映射规则
# 注册ApplyJoinOption字段的映射规则
mapper.register_mapping(
    'groups',
    'ApplyJoinOption',
    lambda x: {
        1: "FreeAccess",#NeedPermission
        2: "FreeAccess",#NeedPermission
        3: "FreeAccess",
        4: "DisableApply"
    }.get(x, "FreeAccess")  # 如果没有匹配的值，返回"未知"
)

# mapper.register_mapping(
#     'groups',
#     'Type',
#     lambda x: "Work" if x == "Private" else x
# )


# 假设data是从数据源中获取的原始数据
# 使用mapper对象的map_data方法来映射数据
# mapped_data = mapper.map_data(data, 'groups', MAPPING_CONFIG['groups'])
