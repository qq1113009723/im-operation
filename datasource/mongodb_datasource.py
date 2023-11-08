import json

from pymongo import MongoClient

import config.config as config
from datasource.datasource import DataSource
from datasource.mapper import field_mapper
from datasource.mapper.mapping_config import MAPPING_CONFIG


def map_fields(data, entity):
    return field_mapper.mapper.map_data(data, entity, MAPPING_CONFIG[entity])
    # mapped_data = []
    # for item in data:
    #     mapped_item = {}
    #     for key, possible_keys in MAPPING_CONFIG[entity].items():
    #         for possible_key in possible_keys:
    #             if possible_key in item:
    #                 mapped_item[key] = item[possible_key]
    #                 break
    #     mapped_data.append(mapped_item)
    # return mapped_data


class MongoDBDataSource(DataSource):
    """
    datasource from mongodb
    """

    def __init__(self, uri=config.MONGO_URI, db_name=config.MONGO_DATABASE_NAME):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_accounts(self, collection_name='im_account'):
        """
        query all im accounts
        :param collection_name: default
        :return: [{}]
        """
        accounts_collection = self.db[collection_name]
        accounts = accounts_collection.find(config.DB_QUERIES['accounts_query'])
        return map_fields(accounts, 'accounts')

    # 实现其他方法...
    def get_groups(self, collection_name='im_group'):
        """
        query all groups
        :param collection_name:
        :return: [{}]
        """
        groups_collection = self.db[collection_name]
        groups = groups_collection.aggregate(config.DB_QUERIES['groups_query'])
        return map_fields(groups, "groups")

    def get_group_ids(self, collection_name='im_group'):
        """
        query all group ids
        :param collection_name:
        :return: list of group ids [str]
        """
        group_members_collection = self.db[collection_name]
        group_ids = group_members_collection.aggregate(config.DB_QUERIES['group_ids_query'])
        return [doc['_id'] for doc in group_ids]

    def get_group_member_ids(self, group_id, collection_name='im_group_member'):
        """
        query im ids of all members under the group_id
        :param group_id: im group id
        :param collection_name: default
        :return: list of member im ids
        """
        group_members_collection = self.db[collection_name]
        conditions = {"imGroupId": group_id}
        # 使用投影来只获取'userImId'字段
        group_members = group_members_collection.find(conditions, {'userImId': 1, '_id': 0})
        # 从查询结果中提取'userImId'
        im_ids = [doc['userImId'] for doc in group_members]
        return im_ids

