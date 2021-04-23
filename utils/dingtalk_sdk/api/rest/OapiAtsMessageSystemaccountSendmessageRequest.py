"""
Created by auto_sdk on 2020.10.27
"""
from api.base import RestApi


class OapiAtsMessageSystemaccountSendmessageRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.content = None
        self.message_biz_code = None
        self.openid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.message.systemaccount.sendmessage'
