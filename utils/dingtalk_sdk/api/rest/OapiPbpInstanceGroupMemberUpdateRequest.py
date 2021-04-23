"""
Created by auto_sdk on 2020.08.25
"""
from api.base import RestApi


class OapiPbpInstanceGroupMemberUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.sync_param = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.pbp.instance.group.member.update'
