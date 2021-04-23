"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiMessageCorpconversationRecallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.msg_task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.corpconversation.recall'
