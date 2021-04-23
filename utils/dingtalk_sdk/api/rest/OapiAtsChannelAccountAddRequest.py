"""
Created by auto_sdk on 2020.08.19
"""
from api.base import RestApi


class OapiAtsChannelAccountAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.channel_user_identify = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.channel.account.add'
