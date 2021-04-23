"""
Created by auto_sdk on 2020.09.21
"""
from api.base import RestApi


class OapiWorkbenchShortcutDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_id = None
        self.biz_no = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workbench.shortcut.delete'
