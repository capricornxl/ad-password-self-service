"""
Created by auto_sdk on 2020.08.17
"""
from api.base import RestApi


class OapiCardIntelligentEmpgroupSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.msg_key = None
        self.param_json = None
        self.receiver_list = None
        self.uuid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.card.intelligent.empgroup.send'
