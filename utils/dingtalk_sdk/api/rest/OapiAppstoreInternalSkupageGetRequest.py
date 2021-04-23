"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAppstoreInternalSkupageGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.callback_page = None
        self.extend_param = None
        self.goods_code = None
        self.item_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.appstore.internal.skupage.get'
