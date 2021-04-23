"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiCspaceAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.code = None
        self.folder_id = None
        self.media_id = None
        self.name = None
        self.overwrite = None
        self.space_id = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.cspace.add'
