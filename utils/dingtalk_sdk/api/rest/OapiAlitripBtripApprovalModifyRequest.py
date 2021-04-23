"""
Created by auto_sdk on 2020.04.06
"""
from api.base import RestApi


class OapiAlitripBtripApprovalModifyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rq = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.approval.modify'
