"""
Created by auto_sdk on 2020.02.23
"""
from api.base import RestApi


class OapiMessageMassSendRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dep_id_list = None
        self.is_preview = None
        self.is_to_all = None
        self.media_id = None
        self.msg_body = None
        self.msg_type = None
        self.text_content = None
        self.unionid = None
        self.userid_list = None
        self.uuid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.message.mass.send'
