"""
Created by auto_sdk on 2021.01.27
"""
from api.base import RestApi


class OapiSceneservicegroupGroupsetCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.group_templateid = None
        self.groupset_name = None
        self.open_teamid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sceneservicegroup.groupset.create'
