"""
Created by auto_sdk on 2021.01.18
"""
from api.base import RestApi


class OapiFinanceLoanBankcardListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.id_card_no = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.bankcard.list'
