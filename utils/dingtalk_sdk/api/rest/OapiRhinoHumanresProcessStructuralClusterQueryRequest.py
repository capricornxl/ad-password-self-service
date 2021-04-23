"""
Created by auto_sdk on 2020.03.06
"""
from api.base import RestApi


class OapiRhinoHumanresProcessStructuralClusterQueryRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_id_process_list = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.humanres.process.structural.cluster.query'
