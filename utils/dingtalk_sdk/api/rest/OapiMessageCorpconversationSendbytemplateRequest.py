"""
Created by auto_sdk on 2021.03.15
"""
from api.base import RestApi


class OapiMessageCorpconversationSendbytemplateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.data = None
        self.dept_id_list = None
        self.template_id = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.corpconversation.sendbytemplate'
