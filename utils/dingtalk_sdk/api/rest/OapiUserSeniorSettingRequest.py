"""
Created by auto_sdk on 2020.12.07
"""
from api.base import RestApi


class OapiUserSeniorSettingRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open = None
        self.permit_staffIds = None
        self.protect_scenes = None
        self.senior_staffId = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.user.senior.setting'
