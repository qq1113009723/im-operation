# 使用示例
import config.config as config
from datasource.mongodb_datasource import MongoDBDataSource
from manager.account_manager import AccountManager

def main():
    data_source = MongoDBDataSource()
    account_manager = AccountManager(data_source)
    accounts_to_create = data_source.query('im_account',config.DB_QUERIES['accounts_delete_query'],'accounts')

    account_manager.delete_concurrently(accounts_to_create)


if __name__ == "__main__":
    main()


