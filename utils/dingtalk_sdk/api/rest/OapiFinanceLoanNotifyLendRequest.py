"""
Created by auto_sdk on 2021.02.25
"""
from api.base import RestApi


class OapiFinanceLoanNotifyLendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.amount_update_time = None
        self.available_limit = None
        self.bank_name = None
        self.bankcard_no = None
        self.bill_date = None
        self.bill_info_list = None
        self.credit_amount = None
        self.daily_interest_rate = None
        self.discounts_id = None
        self.fail_reason = None
        self.fail_reason_to_user = None
        self.first_bill_date = None
        self.first_repay_date = None
        self.id_card_no = None
        self.last_repay_date = None
        self.loan_amount = None
        self.loan_effective_time = None
        self.loan_end_time = None
        self.loan_order_flow_no = None
        self.loan_order_no = None
        self.loan_submit_time = None
        self.loan_txn_time = None
        self.loan_usage = None
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
        self.reduction_total_amount = None
        self.repay_date = None
        self.repay_type = None
        self.status = None
        self.total_term = None
        self.user_mobile = None
        self.year_loan_interest_rate = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.loan.notify.lend'
