"""
Created by auto_sdk on 2021.01.26
"""
from api.base import RestApi


class OapiFinanceFaceVerificationInitRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bio_info = None
        self.cert_name = None
        self.id_card_no = None
        self.scene = None
        self.user_mobile = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.finance.faceVerification.init'
