# 使用示例
from datasource.mongodb_datasource import MongoDBDataSource
from manager.group_manager import GroupManager

def main():
    data_source = MongoDBDataSource()
    group_manager = GroupManager(data_source)
    groups_to_create = data_source.get_groups()  # 获取账号信息的列表

    # 并发创建群组
    results = group_manager.create_concurrently(groups_to_create)

if __name__ == "__main__":
    main()
