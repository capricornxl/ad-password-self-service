"""
Created by auto_sdk on 2020.03.20
"""
from api.base import RestApi


class OapiMessageCorpconversationGetsendresultRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.corpconversation.getsendresult'
