"""
Created by auto_sdk on 2020.03.09
"""
from api.base import RestApi


class OapiProcessinstanceExecuteRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.actioner_userid = None
        self.process_instance_id = None
        self.remark = None
        self.result = None
        self.task_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.processinstance.execute'
