"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiMpdevBuildCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.enable_tabbar = None
        self.main_page = None
        self.miniapp_id = None
        self.package_key = None
        self.package_md5 = None
        self.package_version = None
        self.plugin_refs = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.mpdev.build.create'
