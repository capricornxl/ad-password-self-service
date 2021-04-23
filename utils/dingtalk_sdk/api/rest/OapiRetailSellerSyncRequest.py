"""
Created by auto_sdk on 2019.12.03
"""
from api.base import RestApi


class OapiRetailSellerSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.seller_param = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.retail.seller.sync'
