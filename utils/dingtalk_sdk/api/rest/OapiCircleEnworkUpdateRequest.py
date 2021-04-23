"""
Created by auto_sdk on 2020.02.18
"""
from api.base import RestApi


class OapiCircleEnworkUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_update_dto = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.circle.enwork.update'
