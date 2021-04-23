"""
Created by auto_sdk on 2021.01.26
"""
from api.base import RestApi


class OapiFinanceFaceVerificationUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.business_id = None
        self.fail_reason = None
        self.id_card_no = None
        self.request_code = None
        self.result_code = None
        self.user_mobile = None
        self.verify_result = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.faceVerification.update'
