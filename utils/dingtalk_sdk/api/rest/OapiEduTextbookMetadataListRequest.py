"""
Created by auto_sdk on 2020.12.22
"""
from api.base import RestApi


class OapiEduTextbookMetadataListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.cursor = None
        self.data_order_type = None
        self.level = None
        self.op_user_id = None
        self.parent_id = None
        self.size = None
        self.sort_type = None
        self.subject_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.textbook.metadata.list'
