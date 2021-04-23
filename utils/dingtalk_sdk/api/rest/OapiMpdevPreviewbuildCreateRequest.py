"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiMpdevPreviewbuildCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.build_script_version = None
        self.corpid = None
        self.enable_tabbar = None
        self.ignore_http_req_permission = None
        self.ignore_webview_domain_check = None
        self.main_page = None
        self.miniapp_id = None
        self.package_key = None
        self.page = None
        self.plugin_package_key = None
        self.plugin_refs = None
        self.query = None
        self.sub_packages = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.mpdev.previewbuild.create'
