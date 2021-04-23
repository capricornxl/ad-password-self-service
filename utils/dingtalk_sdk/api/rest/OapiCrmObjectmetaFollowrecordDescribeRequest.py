"""
Created by auto_sdk on 2020.01.07
"""
from api.base import RestApi


class OapiCrmObjectmetaFollowrecordDescribeRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.crm.objectmeta.followrecord.describe'
