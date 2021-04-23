"""
Created by auto_sdk on 2020.01.07
"""
from api.base import RestApi


class OapiRetailSellerOrgdetailQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.retail.seller.orgdetail.query'
