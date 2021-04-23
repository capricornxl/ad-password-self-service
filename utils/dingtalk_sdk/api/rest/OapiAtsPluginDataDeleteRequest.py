"""
Created by auto_sdk on 2020.11.02
"""
from api.base import RestApi


class OapiAtsPluginDataDeleteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.header = None
        self.out_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.plugin.data.delete'
