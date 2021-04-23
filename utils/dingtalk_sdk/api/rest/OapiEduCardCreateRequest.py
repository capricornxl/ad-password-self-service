"""
Created by auto_sdk on 2020.12.31
"""
from api.base import RestApi


class OapiEduCardCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.opencardcreateparam = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.card.create'
