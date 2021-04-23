"""
Created by auto_sdk on 2020.03.09
"""
from api.base import RestApi


class OapiRetailUserBindapplyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.channel = None
        self.request = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.retail.user.bindapply'
