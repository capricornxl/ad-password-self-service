"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiProcessSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.biz_category_id = None
        self.process_name = None
        self.src_process_code = None
        self.target_process_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.process.sync'
