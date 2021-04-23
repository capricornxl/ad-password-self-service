"""
Created by auto_sdk on 2021.01.18
"""
from api.base import RestApi


class OapiFinanceLoanBankcardAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bank_code = None
        self.bank_name = None
        self.bankcard_mobile = None
        self.bankcard_no = None
        self.id_card_no = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.bankcard.add'
