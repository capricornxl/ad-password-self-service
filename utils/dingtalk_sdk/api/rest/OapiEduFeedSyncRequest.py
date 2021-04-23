"""
Created by auto_sdk on 2020.11.23
"""
from api.base import RestApi


class OapiEduFeedSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.album_id = None
        self.dept_id = None
        self.fee_type = None
        self.feed_medias = None
        self.future = None
        self.media_uid = None
        self.op_userId = None
        self.send_time = None
        self.send_uid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.feed.sync'
