"""
Created by auto_sdk on 2021.04.09
"""
from api.base import RestApi


class OapiExtcontactGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.user_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.extcontact.get'
