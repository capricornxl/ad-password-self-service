"""
Created by auto_sdk on 2020.03.09
"""
from api.base import RestApi


class OapiRetailUserUnbindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.associate_union_id = None
        self.channel = None
        self.outer_id = None
        self.sub_outer_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.retail.user.unbind'
