"""
Created by auto_sdk on 2019.07.19
"""
from api.base import RestApi


class OapiMessageMassRecallRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.task_id = None
        self.unionid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.mass.recall'
