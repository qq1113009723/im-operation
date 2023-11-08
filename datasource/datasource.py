from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    def get_accounts(self):
        pass

    @abstractmethod
    def get_groups(self):
        pass

    @abstractmethod
    def get_group_ids(self):
        pass

    @abstractmethod
    def get_group_member_ids(self, group_id):
        pass