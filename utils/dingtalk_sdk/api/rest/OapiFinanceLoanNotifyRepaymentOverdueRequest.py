"""
Created by auto_sdk on 2021.02.05
"""
from api.base import RestApi


class OapiFinanceLoanNotifyRepaymentOverdueRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current_unpaid_interest = None
        self.current_unpaid_penalty = None
        self.current_unpaid_principal = None
        self.current_unpaid_total_amount = None
        self.id_card_no = None
        self.int_ovd_days = None
        self.loan_order_no = None
        self.open_channel_name = None
        self.open_product_name = None
        self.ovd_terms = None
        self.paid_interest = None
        self.paid_penalty = None
        self.paid_principal = None
        self.paid_total_amount = None
        self.payable_interest = None
        self.payable_penalty = None
        self.payable_principal = None
        self.payable_total_amount = None
        self.period_paid_interest = None
        self.period_paid_penalty = None
        self.period_paid_principal = None
        self.period_paid_total_amount = None
        self.period_payable_interest = None
        self.period_payable_penalty = None
        self.period_payable_principal = None
        self.period_payable_total_amount = None
        self.prin_ovd_days = None
        self.repay_real_date = None
        self.repayment_terms = None
        self.send_ding_ding_msg = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.notify.repayment.overdue'
