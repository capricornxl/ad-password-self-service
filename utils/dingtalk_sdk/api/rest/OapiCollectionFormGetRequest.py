"""
Created by auto_sdk on 2020.06.16
"""
from api.base import RestApi


class OapiCollectionFormGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_date = None
        self.form_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.collection.form.get'
