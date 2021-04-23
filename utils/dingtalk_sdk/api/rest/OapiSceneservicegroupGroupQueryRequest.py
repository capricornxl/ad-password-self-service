"""
Created by auto_sdk on 2021.01.21
"""
from api.base import RestApi


class OapiSceneservicegroupGroupQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.group_name = None
        self.open_conversationid = None
        self.open_groupsetid = None
        self.open_teamid = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sceneservicegroup.group.query'
