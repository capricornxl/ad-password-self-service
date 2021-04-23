"""
Created by auto_sdk on 2020.12.22
"""
from api.base import RestApi


class OapiEduGroupMsgSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.biz_id = None
        self.class_id = None
        self.image_url = None
        self.receive_userid_list = None
        self.replace = None
        self.template_code = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.group.msg.send'
