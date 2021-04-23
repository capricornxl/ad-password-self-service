"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpMessageCorpconversationAsyncsendbycodeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.code = None
        self.dept_id_list = None
        self.msgcontent = None
        self.msgtype = None
        self.to_all_user = None
        self.user_id_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.message.corpconversation.asyncsendbycode'
