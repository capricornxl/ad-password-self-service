"""
Created by auto_sdk on 2019.12.30
"""
from api.base import RestApi


class OapiEduTypeDataGetRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.orders = None
        self.page_num = None
        self.page_size = None
        self.stat_date = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.edu.type.data.get'
