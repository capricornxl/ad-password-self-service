"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiCcoserviceServicegroupUpdateservicetimeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.end_time = None
        self.open_conversation_id = None
        self.start_time = None
        self.time_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ccoservice.servicegroup.updateservicetime'
