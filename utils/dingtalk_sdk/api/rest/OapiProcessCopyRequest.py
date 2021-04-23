"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiProcessCopyRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.biz_category_id = None
        self.copy_type = None
        self.description = None
        self.process_code = None
        self.process_name = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.copy'
