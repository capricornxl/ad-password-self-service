"""
Created by auto_sdk on 2021.02.02
"""
from api.base import RestApi


class OapiWorkspaceProjectAssistantSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_url = None
        self.content = None
        self.pic_url = None
        self.reciever_userids = None
        self.style = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.project.assistant.send'
