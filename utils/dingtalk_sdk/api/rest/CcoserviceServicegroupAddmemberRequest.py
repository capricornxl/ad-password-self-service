"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CcoserviceServicegroupAddmemberRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.open_group_id = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.ccoservice.servicegroup.addmember'
