"""
Created by auto_sdk on 2021.03.22
"""
from api.base import RestApi


class OapiKacOpenliveRecordListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.author_user_id = None
        self.begin_time = None
        self.end_time = None
        self.page_size = None
        self.page_start = None
        self.status = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.kac.openlive.record.list'
