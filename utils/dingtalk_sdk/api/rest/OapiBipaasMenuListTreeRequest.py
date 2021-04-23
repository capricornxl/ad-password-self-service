"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiBipaasMenuListTreeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.antcloud_tenant_id = None
        self.published = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.bipaas.menu.list_tree'
