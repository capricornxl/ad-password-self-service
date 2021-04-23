"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiProcessTemplateUpgradeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.detail_component_id = None
        self.form_component_id = None
        self.process_code = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.template.upgrade'
