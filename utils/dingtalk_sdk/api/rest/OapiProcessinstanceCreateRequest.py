"""
Created by auto_sdk on 2020.12.09
"""
from api.base import RestApi


class OapiProcessinstanceCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.approvers = None
        self.approvers_v2 = None
        self.cc_list = None
        self.cc_position = None
        self.dept_id = None
        self.form_component_values = None
        self.originator_user_id = None
        self.process_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.processinstance.create'
