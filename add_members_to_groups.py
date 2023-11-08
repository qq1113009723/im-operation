# 使用示例
from datasource.mongodb_datasource import MongoDBDataSource
from manager.group_member_manager import GroupMemberManager

if __name__ == "__main__":

    data_source = MongoDBDataSource()
    group_member_manager = GroupMemberManager(data_source)
    group_ids_to_add_member = data_source.get_group_ids()  # 获取账号信息的列表

    # 并发为群添加成员
    results = group_member_manager.create_concurrently(group_ids_to_add_member)