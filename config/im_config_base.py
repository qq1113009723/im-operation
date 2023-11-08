import random

import TLSSigAPIv2

import config.config as config


class IMConfigBase:
    def __init__(self):
        self.sdk_app_id = config.IM_CONFIG['sdk_app_id']
        self.secret_key = config.IM_CONFIG['secret_key']
        self.admin_account = config.IM_CONFIG['admin_account']
        self.api = TLSSigAPIv2.TLSSigAPIv2(int(self.sdk_app_id), self.secret_key)
        self.cached_user_sig = None  # 添加一个属性来缓存UserSig

    def generate_user_sig(self, user_id=None, expire=180 * 86400, force_refresh=False):
        """
        Generate UserSig for a specific user ID or admin account if no user ID is provided.

        :param force_refresh:
        :param user_id: The user ID for which to generate the UserSig. If None, use admin account.
        :param expire: The expiration time of the UserSig in seconds. Default is 180 days.
        :return: A string of UserSig.
        """
        if force_refresh or not self.cached_user_sig:
            user_id = user_id if user_id else self.admin_account
            self.cached_user_sig = self.api.gen_sig(user_id, expire)
        return self.cached_user_sig

    def generate_request_params(self, refresh_user_sig=False):
        user_sig = self.generate_user_sig(force_refresh=refresh_user_sig)

        return {
            "sdkappid": self.sdk_app_id,
            "identifier": self.admin_account,
            "usersig": user_sig,
            "random": random.randint(0, 4294967295),
            "contenttype": "json"
        }

    def generate_request_header(self):
        return {
            'Content-Type': 'application/json'
        }
# Example usage:
# im_base = IMBase()
# user_sig = im_base.generate_user_sig()
# print(user_sig)
