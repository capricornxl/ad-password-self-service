"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class IsvCallCalluserRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.authed_corp_id = None
        self.authed_staff_id = None
        self.staff_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.isv.call.calluser'
