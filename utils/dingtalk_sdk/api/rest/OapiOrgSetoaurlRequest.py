"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiOrgSetoaurlRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.oa_title = None
        self.oa_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.org.setoaurl'
