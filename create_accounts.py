# 使用示例
from datasource.mongodb_datasource import MongoDBDataSource
from manager.account_manager import AccountManager

if __name__ == "__main__":

    data_source = MongoDBDataSource()
    account_manager = AccountManager(data_source)
    accounts_to_create = data_source.get_accounts()  # 获取账号信息的列表

    # 并发创建账号
    results = account_manager.create_concurrently(accounts_to_create)