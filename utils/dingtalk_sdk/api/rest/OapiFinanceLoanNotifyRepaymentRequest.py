"""
Created by auto_sdk on 2021.02.05
"""
from api.base import RestApi


class OapiFinanceLoanNotifyRepaymentRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.amount = None
        self.available_amount = None
        self.bank_name = None
        self.bankcard_no = None
        self.current_int_ovd_days = None
        self.current_ovd_terms = None
        self.current_paid_interest = None
        self.current_paid_penalty = None
        self.current_paid_principal = None
        self.current_paid_total_amount = None
        self.current_prin_ovd_days = None
        self.fail_reason = None
        self.fail_reason_to_user = None
        self.id_card_no = None
        self.loan_order_no = None
        self.open_channel_name = None
        self.open_product_code = None
        self.open_product_name = None
        self.open_product_type = None
        self.paid_interest = None
        self.paid_penalty = None
        self.paid_principal = None
        self.paid_total_amount = None
        self.payable_interest = None
        self.payable_penalty = None
        self.payable_principal = None
        self.payable_total_amount = None
        self.period_paid_all = None
        self.period_paid_interest = None
        self.period_paid_penalty = None
        self.period_paid_principal = None
        self.period_paid_total_amount = None
        self.period_payable_interest = None
        self.period_payable_penalty = None
        self.period_payable_principal = None
        self.period_payable_total_amount = None
        self.repay_real_date = None
        self.repay_type = None
        self.repayment_no = None
        self.repayment_terms = None
        self.status = None
        self.type = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.notify.repayment'
