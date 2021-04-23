"""
Created by auto_sdk on 2020.06.28
"""
from api.base import RestApi


class OapiDdpaasObjectmetaDescribeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_uuid = None
        self.form_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ddpaas.objectmeta.describe'
