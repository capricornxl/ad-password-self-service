"""
Created by auto_sdk on 2020.12.04
"""
from api.base import RestApi


class OapiFinanceLoanQualificationGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.code = None
        self.open_channel_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.qualification.get'
