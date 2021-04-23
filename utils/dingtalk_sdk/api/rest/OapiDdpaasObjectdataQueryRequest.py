"""
Created by auto_sdk on 2020.06.28
"""
from api.base import RestApi


class OapiDdpaasObjectdataQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_uuid = None
        self.current_operator_userid = None
        self.cursor = None
        self.form_code = None
        self.query_dsl = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ddpaas.objectdata.query'
