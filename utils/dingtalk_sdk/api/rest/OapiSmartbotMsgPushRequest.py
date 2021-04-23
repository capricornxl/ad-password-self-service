"""
Created by auto_sdk on 2021.03.19
"""
from api.base import RestApi


class OapiSmartbotMsgPushRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id_list = None
        self.msg = None
        self.to_all_user = None
        self.user_id_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartbot.msg.push'
