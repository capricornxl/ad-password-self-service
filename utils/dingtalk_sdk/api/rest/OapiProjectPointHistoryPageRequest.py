"""
Created by auto_sdk on 2020.12.28
"""
from api.base import RestApi


class OapiProjectPointHistoryPageRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.page_size = None
        self.tenant_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.project.point.history.page'
