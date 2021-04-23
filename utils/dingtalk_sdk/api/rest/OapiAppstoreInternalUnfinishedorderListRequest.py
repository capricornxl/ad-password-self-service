"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiAppstoreInternalUnfinishedorderListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.item_code = None
        self.page = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.appstore.internal.unfinishedorder.list'
