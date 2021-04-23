"""
Created by auto_sdk on 2020.06.10
"""
from api.base import RestApi


class OapiWorkspaceTestappInstallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.install_testapp = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workspace.testapp.install'
