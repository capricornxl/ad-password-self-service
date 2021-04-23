"""
Created by auto_sdk on 2020.11.30
"""
from api.base import RestApi


class OapiRhinoTransportMaplocationQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.include_config = None
        self.poi_code_list = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.transport.maplocation.query'
