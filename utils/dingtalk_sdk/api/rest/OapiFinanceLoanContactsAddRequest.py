"""
Created by auto_sdk on 2021.01.18
"""
from api.base import RestApi


class OapiFinanceLoanContactsAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.contact_mobile = None
        self.id_card_no = None
        self.user_category = None
        self.user_mobile = None
        self.user_name = None
        self.user_relation = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.contacts.add'
