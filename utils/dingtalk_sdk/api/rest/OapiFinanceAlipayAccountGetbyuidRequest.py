"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiFinanceAlipayAccountGetbyuidRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.alipay.account.getbyuid'
