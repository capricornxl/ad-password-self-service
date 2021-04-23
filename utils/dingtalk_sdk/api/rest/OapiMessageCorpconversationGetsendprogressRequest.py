"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiMessageCorpconversationGetsendprogressRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.corpconversation.getsendprogress'
