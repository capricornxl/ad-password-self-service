"""
Created by auto_sdk on 2021.04.13
"""
from api.base import RestApi


class OapiSceneservicegroupGroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bizid = None
        self.group_name = None
        self.group_tag_names = None
        self.group_tagids = None
        self.member_staffids = None
        self.open_groupsetid = None
        self.open_teamid = None
        self.owner_staffId = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.sceneservicegroup.group.create'
