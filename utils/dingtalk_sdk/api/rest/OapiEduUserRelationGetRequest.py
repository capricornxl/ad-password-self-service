"""
Created by auto_sdk on 2021.01.29
"""
from api.base import RestApi


class OapiEduUserRelationGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.class_id = None
        self.from_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.user.relation.get'
