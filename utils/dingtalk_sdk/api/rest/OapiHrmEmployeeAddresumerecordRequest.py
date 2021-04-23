"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiHrmEmployeeAddresumerecordRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.content = None
        self.k_v_content = None
        self.pc_url = None
        self.phone_url = None
        self.record_timestamp = None
        self.title = None
        self.userid = None
        self.web_url = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.hrm.employee.addresumerecord'
