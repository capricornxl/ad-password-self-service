"""
Created by auto_sdk on 2021.04.15
"""
from api.base import RestApi


class OapiEduClassListbyteacherRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.filter_param = None
        self.queryFromAllOrgs = None
        self.ret_ext_fields = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.class.listbyteacher'
