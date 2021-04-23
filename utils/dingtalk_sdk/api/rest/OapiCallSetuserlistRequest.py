"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiCallSetuserlistRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.staff_id_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.call.setuserlist'
