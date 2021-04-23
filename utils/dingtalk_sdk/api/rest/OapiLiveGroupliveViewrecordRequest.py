"""
Created by auto_sdk on 2020.12.07
"""
from api.base import RestApi


class OapiLiveGroupliveViewrecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dept_id = None
        self.live_uuid = None
        self.page_index = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.live.grouplive.viewrecord'
