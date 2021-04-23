"""
Created by auto_sdk on 2021.01.18
"""
from api.base import RestApi


class OapiCrmContactCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.contact_name = None
        self.contact_phone = None
        self.contact_position_list = None
        self.creator_userid = None
        self.customer_instance_id = None
        self.provider_corpid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.contact.create'
