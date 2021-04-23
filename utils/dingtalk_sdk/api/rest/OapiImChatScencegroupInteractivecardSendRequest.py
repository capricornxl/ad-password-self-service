"""
Created by auto_sdk on 2021.01.11
"""
from api.base import RestApi


class OapiImChatScencegroupInteractivecardSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.card_mediaid_param_map = None
        self.card_param_map = None
        self.card_template_id = None
        self.out_track_id = None
        self.receiver_userid_list = None
        self.robot_code = None
        self.target_open_conversation_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.im.chat.scencegroup.interactivecard.send'
