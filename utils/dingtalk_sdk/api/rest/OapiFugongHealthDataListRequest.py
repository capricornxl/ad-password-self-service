"""
Created by auto_sdk on 2020.03.02
"""
from api.base import RestApi


class OapiFugongHealthDataListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.action_date = None
        self.offset = None
        self.process_instance_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.fugong.health_data.list'
