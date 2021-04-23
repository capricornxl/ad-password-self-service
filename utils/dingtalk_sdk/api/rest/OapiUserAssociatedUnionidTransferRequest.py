"""
Created by auto_sdk on 2020.01.14
"""
from api.base import RestApi


class OapiUserAssociatedUnionidTransferRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.associated_unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.associated_unionid.transfer'
