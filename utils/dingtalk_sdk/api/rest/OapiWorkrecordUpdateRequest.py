"""
Created by auto_sdk on 2020.12.08
"""
from api.base import RestApi


class OapiWorkrecordUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.record_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workrecord.update'
