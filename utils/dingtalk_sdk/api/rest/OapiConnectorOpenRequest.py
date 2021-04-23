"""
Created by auto_sdk on 2020.11.05
"""
from api.base import RestApi


class OapiConnectorOpenRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.connector_id = None
        self.corp_id = None
        self.creator_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.connector.open'
