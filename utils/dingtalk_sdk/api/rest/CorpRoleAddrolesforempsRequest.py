"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpRoleAddrolesforempsRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.rolelid_list = None
        self.userid_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.role.addrolesforemps'
