"""
Created by auto_sdk on 2021.01.22
"""
from api.base import RestApi


class OapiMessageCorpconversationStatusBarUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.status_bg = None
        self.status_value = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.corpconversation.status_bar.update'
