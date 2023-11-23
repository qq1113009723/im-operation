import json
import logging

import openpyxl
import requests

import config.config as config
from misc import thread_safety
from datasource.datasource import DataSource
from config.im_config_base import IMConfigBase
from manager.account_manager import lock
from manager.creator import Creator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@thread_safety.thread_safe_function(lock)
def write_result_to_excel(group_info, result):
    file = "results_group_creation.xlsx"
    # 检查是否存在Excel文件，如果不存在则创建
    try:
        wb = openpyxl.load_workbook(file)
    except FileNotFoundError:
        # 如果文件不存在，创建一个新的工作簿和表单
        wb = openpyxl.Workbook()
        sheet = wb.active
        # 添加标题行
        sheet.append(
            ['GroupId', 'Owner_Account', 'Type', 'Name',  # 'FaceUrl,', 'MaxMemberCount', 'ApplyJoinOption,',
             'ErrorCode',
             'ErrorInfo']
        )
    else:
        # 如果文件存在，获取活动的工作表
        sheet = wb.active

    # 添加数据行
    sheet.append([
        group_info.get('GroupId', ''),
        group_info.get('Owner_Account', ''),
        group_info.get('Type', ''),
        group_info.get('Name', ''),
        # group_info.get('FaceUrl', ''),
        # group_info.get('MaxMemberCount', ''),
        #  group_info.get('ApplyJoinOption', ''),
        result.get('ErrorCode', ''),
        result.get('ErrorInfo', '')
    ])
    # 保存Excel文件
    wb.save(file)


class GroupManager(Creator, IMConfigBase):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.api_url = config.IM_APIS['create_group']
        self.admin_sig = self.generate_user_sig()

    def create_one(self, group_info):
        # 构造请求体
        payload = {
            "GroupId": group_info['GroupId'],
            "Owner_Account": group_info['Owner_Account'],
            "Type": group_info['Type'],
            "Name": group_info['Name']
            # "FaceUrl": group_info['FaceUrl'],
            # "MaxMemberCount": group_info['MaxMemberCount']
            # "ApplyJoinOption": group_info['ApplyJoinOption']
        }

        # Send the request to the IM service
        response = requests.post(self.api_url, params=self.generate_request_params(), headers=self.generate_request_header(), data=json.dumps(payload))

        result = response.json()
        logger.info(f"Account creation result for group ID {group_info['GroupId']}: {result}")
        # 将结果写入Excel
        # write_result_to_excel(group_info, result)
        return result
