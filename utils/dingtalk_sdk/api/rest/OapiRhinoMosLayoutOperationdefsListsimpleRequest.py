"""
Created by auto_sdk on 2020.07.16
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefsListsimpleRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.operation_uids = None
        self.order_id = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdefs.listsimple'
