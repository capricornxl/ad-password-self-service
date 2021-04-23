"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpHrmEmployeeDelemployeedismissionandhandoverRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.dismission_info_with_hand_over = None
        self.op_userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.hrm.employee.delemployeedismissionandhandover'
