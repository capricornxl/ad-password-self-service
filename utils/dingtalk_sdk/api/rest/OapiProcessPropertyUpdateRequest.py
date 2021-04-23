"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiProcessPropertyUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.component_id = None
        self.process_code = None
        self.props = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.property.update'
