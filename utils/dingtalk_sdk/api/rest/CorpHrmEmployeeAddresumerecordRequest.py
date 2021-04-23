"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class CorpHrmEmployeeAddresumerecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.content = None
        self.k_v_content = None
        self.pc_url = None
        self.phone_url = None
        self.record_time_stamp = None
        self.title = None
        self.userid = None
        self.web_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.hrm.employee.addresumerecord'
