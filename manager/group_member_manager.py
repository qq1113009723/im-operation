import json
import logging

import openpyxl
import requests

import config.config as config
from config.im_config_base import IMConfigBase
from datasource.datasource import DataSource
from manager.account_manager import lock
from manager.creator import Creator
from misc.thread_safety import thread_safe_function

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@thread_safe_function(lock)
def write_result_to_excel(payload, result):
    file = "results_group_member_addition.xlsx"
    try:
        wb = openpyxl.load_workbook(file)
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(['GroupId', 'Member_Account', 'ErrorCode', 'ErrorInfo'])
    else:
        sheet = wb.active

        # 遍历成员列表，为每个成员添加一行
    for member in payload.get('MemberList', []):
        member_account = member.get('Member_Account', '')  # 获取成员账号
        sheet.append([
            payload.get('GroupId', ''),
            member_account,
            result.get('ErrorCode', ''),
            result.get('ErrorInfo', '')
        ])
    wb.save(file)


class GroupMemberManager(Creator, IMConfigBase):

    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.api_url = config.IM_APIS['add_group_member']

    def get_members_by_group_id(self, group_id):
        # 从MongoDB中查询属于特定组的所有成员
        return list(self.data_source.get_group_member_ids(group_id))

    def create_one(self, group_id):
        members = self.get_members_by_group_id(group_id)
        # 分批处理，每批最多100个成员
        batch_size = 100
        result = []
        for i in range(0, len(members), batch_size):
            batch = members[i:i + batch_size]
            member_list = [{"Member_Account": member_id} for member_id in batch]
            result.append(self.add_member_to_group(group_id, member_list))
        return result

    def add_member_to_group(self, group_id, member_list):
        payload = {
            "GroupId": group_id,
            "MemberList": member_list
        }
        # Send the request to the IM service
        response = requests.post(self.api_url, params=self.generate_request_params(),
                                 headers=self.generate_request_header(), data=json.dumps(payload))

        result = response.json()
        logger.info(f"Add member to group result for payload: {payload}: {result}")
        write_result_to_excel(payload, result)
        # 将结果写入Excel
        return result
