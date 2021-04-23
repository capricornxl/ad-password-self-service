"""
Created by auto_sdk on 2021.01.26
"""
from api.base import RestApi


class OapiFinanceFaceVerificationQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.business_id = None
        self.id_card_no = None
        self.request_code = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.faceVerification.query'
