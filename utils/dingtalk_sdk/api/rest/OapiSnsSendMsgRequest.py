"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSnsSendMsgRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.code = None
        self.msg = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sns.send_msg'
