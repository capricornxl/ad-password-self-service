"""
Created by auto_sdk on 2019.07.25
"""
from api.base import RestApi


class OapiDingSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_ding_send_vo = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ding.send'
