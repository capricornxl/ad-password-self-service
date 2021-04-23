"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiCallbackFailrecordListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.req = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.callback.failrecord.list'
