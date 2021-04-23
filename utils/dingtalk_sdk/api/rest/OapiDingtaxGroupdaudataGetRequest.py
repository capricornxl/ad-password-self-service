"""
Created by auto_sdk on 2020.12.03
"""
from api.base import RestApi


class OapiDingtaxGroupdaudataGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_conversation_id_list = None
        self.stat_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingtax.groupdaudata.get'
