"""
Created by auto_sdk on 2020.01.20
"""
from api.base import RestApi


class OapiUserCorpinfoListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.corp_name = None
        self.mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.corpinfo.list'
