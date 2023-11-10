import json
import logging

import openpyxl
import requests

import config.config as config
from misc import thread_safety
from datasource.datasource import DataSource
from config.im_config_base import IMConfigBase
from manager.creator import Creator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from threading import Lock

# 创建一个锁对象
lock = Lock()
@thread_safety.thread_safe_function(lock)
def write_result_to_excel(account_info, result):
    # 检查是否存在Excel文件，如果不存在则创建
    file = "results_account_creation.xlsx"
    try:
        wb = openpyxl.load_workbook(file)
    except FileNotFoundError:
        # 如果文件不存在，创建一个新的工作簿和表单
        wb = openpyxl.Workbook()
        sheet = wb.active
        # 添加标题行
        sheet.append(['UserID', 'Nick', 'FaceUrl', 'ErrorCode', 'ErrorInfo'])
    else:
        # 如果文件存在，获取活动的工作表
        sheet = wb.active

    # 添加数据行
    sheet.append([
        account_info.get('UserID', ''),
        account_info.get('Nick', ''),
        account_info.get('FaceUrl', ''),
        result.get('ErrorCode', ''),
        result.get('ErrorInfo', '')
    ])
    # 保存Excel文件
    wb.save(file)


class AccountManager(Creator, IMConfigBase):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.api_url = config.IM_APIS['account_import']
        self.admin_sig = self.generate_user_sig()

    def create_one(self, account_info):
        # 构造请求体
        payload = {
            "UserID": account_info['UserID'],
            "Nick": account_info['Nick'],
            "FaceUrl": account_info['FaceUrl']
        }

        # 发起POST请求
        response = requests.post(self.api_url, headers=self.generate_request_header(),
                                 params=self.generate_request_params(), data=json.dumps(payload))
        result = response.json()
        logger.info(f"Account creation result for user ID {account_info['UserID']}: {result}")
        # 将结果写入Excel
        write_result_to_excel(account_info, result)
        return result
