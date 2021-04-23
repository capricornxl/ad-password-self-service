"""
Created by auto_sdk on 2019.08.08
"""
from api.base import RestApi


class OapiWorkbenchShortcutListbypagingRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.page_index = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.workbench.shortcut.listbypaging'
