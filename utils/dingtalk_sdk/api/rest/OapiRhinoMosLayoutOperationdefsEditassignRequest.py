"""
Created by auto_sdk on 2020.03.23
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefsEditassignRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.assign_info_modify_items = None
        self.order_id = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdefs.editassign'
