"""
Created by auto_sdk on 2020.12.30
"""
from api.base import RestApi


class OapiMicroappCustomUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.app_corp_id = None
        self.desc = None
        self.homepage_link = None
        self.icon = None
        self.ip_white_list = None
        self.name = None
        self.omp_link = None
        self.pc_homepage_link = None
        self.top_related_corp_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.microapp.custom.update'
