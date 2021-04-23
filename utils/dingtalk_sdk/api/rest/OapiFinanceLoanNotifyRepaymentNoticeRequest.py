"""
Created by auto_sdk on 2021.02.05
"""
from api.base import RestApi


class OapiFinanceLoanNotifyRepaymentNoticeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.id_card_no = None
        self.loan_order_no = None
        self.open_channel_name = None
        self.open_product_name = None
        self.ovd_terms = None
        self.paid_interest = None
        self.paid_penalty = None
        self.paid_principal = None
        self.paid_total_amount = None
        self.repay_real_date = None
        self.repayment_terms = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.notify.repayment.notice'
