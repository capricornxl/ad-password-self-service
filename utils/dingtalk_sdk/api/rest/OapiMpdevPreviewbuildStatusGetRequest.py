"""
Created by auto_sdk on 2020.10.15
"""
from api.base import RestApi


class OapiMpdevPreviewbuildStatusGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.miniapp_id = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.mpdev.previewbuild.status.get'
