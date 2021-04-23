"""
Created by auto_sdk on 2020.01.06
"""
from api.base import RestApi


class OapiMcsConferenceCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_key = None
        self.is_push_record = None
        self.preference_region = None
        self.room_valid_time = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.mcs.conference.create'
