"""
Created by auto_sdk on 2020.12.24
"""
from api.base import RestApi


class OapiImChatScenegroupTemplateApplyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.apply_mode = None
        self.open_conversation_id = None
        self.owner_user_id = None
        self.template_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scenegroup.template.apply'
