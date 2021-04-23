"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiChatTransformRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.chat.transform'
