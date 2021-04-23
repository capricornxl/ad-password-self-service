"""
Created by auto_sdk on 2021.03.24
"""
from api.base import RestApi


class OapiWorkbenchShortcutAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_id = None
        self.biz_no = None
        self.icon = None
        self.name = None
        self.pc_shortcut_uri = None
        self.shortcut_uri = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workbench.shortcut.add'
