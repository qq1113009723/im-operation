# datasource/excel_datasource.py
from abc import ABC

import pandas as pd
from datasource.datasource import DataSource
from datasource.mapper.mapping_config import MAPPING_CONFIG


class ExcelDataSource(DataSource, ABC):

    def __init__(self, file_path):
        self.file_path = file_path

    def map_fields(self, df, entity):
        mapped_df = pd.DataFrame()
        for key, possible_keys in MAPPING_CONFIG[entity].items():
            for possible_key in possible_keys:
                if possible_key in df.columns:
                    mapped_df[key] = df[possible_key]
                    break
        return mapped_df

    def get_accounts(self,sheet_name='accounts'):
        df = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return self.map_fields(df, 'accounts').to_dict('records')

    # 实现其他方法...
    def get_groups(self):
        pass

    def get_group_member_ids(self):
        pass
