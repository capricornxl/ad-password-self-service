"""
Created by auto_sdk on 2019.10.31
"""
from api.base import RestApi


class OapiRetailSellerQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.retail.seller.query'
