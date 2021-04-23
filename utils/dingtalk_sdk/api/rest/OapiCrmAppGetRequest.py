"""
Created by auto_sdk on 2020.09.24
"""
from api.base import RestApi


class OapiCrmAppGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_key = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.app.get'
