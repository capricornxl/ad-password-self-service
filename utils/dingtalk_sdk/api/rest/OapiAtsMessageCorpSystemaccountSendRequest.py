"""
Created by auto_sdk on 2020.12.01
"""
from api.base import RestApi


class OapiAtsMessageCorpSystemaccountSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.message.corp.systemaccount.send'
