"""
Created by auto_sdk on 2021.01.21
"""
from api.base import RestApi


class OapiSceneservicegroupMessageSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.at_dingtalkids = None
        self.at_mobiles = None
        self.at_unionids = None
        self.bizid = None
        self.btn_orientation = None
        self.btns = None
        self.content = None
        self.is_at_all = None
        self.message_type = None
        self.open_conversationid = None
        self.receiver_dingtalkids = None
        self.receiver_mobiles = None
        self.receiver_unionids = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sceneservicegroup.message.send'
