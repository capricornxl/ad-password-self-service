"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiDingpayBillBatchquerycountRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.apply_pay_operator_userid = None
        self.bill_category = None
        self.biz_code = None
        self.create_operator_userid = None
        self.extension = None
        self.gmt_apply_pay_begin_time = None
        self.gmt_apply_pay_end_time = None
        self.gmt_create_begin_time = None
        self.gmt_create_end_time = None
        self.gmt_pay_begin_time = None
        self.gmt_pay_end_time = None
        self.max_amount = None
        self.min_amount = None
        self.pay_channel_list = None
        self.pay_channel_payer_real_uid = None
        self.payee_id = None
        self.payee_user_type = None
        self.payer_id = None
        self.payer_user_type = None
        self.receiptor_type_list = None
        self.status_list = None
        self.termination_reason = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.dingpay.bill.batchquerycount'
