"""
Created by auto_sdk on 2020.07.09
"""
from api.base import RestApi


class OapiProjectInviteShareurlGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.invite_info = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.project.invite.shareurl.get'
