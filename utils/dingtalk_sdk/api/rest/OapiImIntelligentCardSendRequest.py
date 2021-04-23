"""
Created by auto_sdk on 2019.09.26
"""
from api.base import RestApi


class OapiImIntelligentCardSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.open_conversation_id = None
        self.template_data = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.intelligent.card.send'
