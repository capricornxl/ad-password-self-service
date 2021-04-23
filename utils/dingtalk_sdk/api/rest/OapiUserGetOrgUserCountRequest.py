"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiUserGetOrgUserCountRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.onlyActive = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.user.get_org_user_count'
