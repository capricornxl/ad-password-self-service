"""
Created by auto_sdk on 2020.10.14
"""
from api.base import RestApi


class OapiEduSubjectMetadataListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.area_code = None
        self.cursor = None
        self.data_order_type = None
        self.level = None
        self.operator_userid = None
        self.parent_id = None
        self.period_code = None
        self.size = None
        self.sort_type = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.subject.metadata.list'
