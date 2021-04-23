"""
Created by auto_sdk on 2020.06.16
"""
from api.base import RestApi


class OapiCollectionFormListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.creator = None
        self.offset = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.collection.form.list'
