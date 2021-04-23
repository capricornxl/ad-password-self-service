"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiUserBatchdeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.useridlist = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.batchdelete'
