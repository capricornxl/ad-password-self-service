"""
Created by auto_sdk on 2020.07.01
"""
from api.base import RestApi


class OapiCollectionInstanceGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_type = None
        self.formInstance_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.collection.instance.get'
