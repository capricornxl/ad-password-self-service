"""
Created by auto_sdk on 2020.11.12
"""
from api.base import RestApi


class OapiMicroappCustomCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.app_corp_id = None
        self.desc = None
        self.develop_type = None
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
        return 'dingtalk.oapi.microapp.custom.create'
