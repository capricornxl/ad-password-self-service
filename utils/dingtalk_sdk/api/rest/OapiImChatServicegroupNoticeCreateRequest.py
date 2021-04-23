"""
Created by auto_sdk on 2019.12.04
"""
from api.base import RestApi


class OapiImChatServicegroupNoticeCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.chat_id = None
        self.send_ding = None
        self.sticky = None
        self.text_content = None
        self.title = None
        self.unique_key = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.servicegroup.notice.create'
