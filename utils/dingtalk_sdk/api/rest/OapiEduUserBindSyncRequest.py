"""
Created by auto_sdk on 2020.12.18
"""
from api.base import RestApi


class OapiEduUserBindSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.user.bind.sync'
