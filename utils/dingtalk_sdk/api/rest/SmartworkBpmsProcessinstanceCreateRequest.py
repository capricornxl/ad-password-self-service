"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class SmartworkBpmsProcessinstanceCreateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.approvers = None
        self.cc_list = None
        self.cc_position = None
        self.dept_id = None
        self.form_component_values = None
        self.originator_user_id = None
        self.process_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.smartwork.bpms.processinstance.create'
