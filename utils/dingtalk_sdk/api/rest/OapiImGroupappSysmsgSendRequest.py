"""
Created by auto_sdk on 2020.06.30
"""
from api.base import RestApi


class OapiImGroupappSysmsgSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.msg_key = None
        self.msg_param = None
        self.open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.groupapp.sysmsg.send'
