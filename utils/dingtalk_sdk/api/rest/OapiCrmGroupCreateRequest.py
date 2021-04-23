"""
Created by auto_sdk on 2020.05.19
"""
from api.base import RestApi


class OapiCrmGroupCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.colleague_userid_list = None
        self.contact_id_list = None
        self.customer_corpid = None
        self.customer_id = None
        self.group_owner = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.group.create'
