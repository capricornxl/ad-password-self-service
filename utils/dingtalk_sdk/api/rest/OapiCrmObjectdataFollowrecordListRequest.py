"""
Created by auto_sdk on 2020.02.14
"""
from api.base import RestApi


class OapiCrmObjectdataFollowrecordListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.current_operator_userid = None
        self.data_id_list = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectdata.followrecord.list'
