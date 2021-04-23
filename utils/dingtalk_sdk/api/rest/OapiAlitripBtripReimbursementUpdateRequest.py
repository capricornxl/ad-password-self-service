"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiAlitripBtripReimbursementUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rq = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.alitrip.btrip.reimbursement.update'
