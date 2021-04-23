"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class CorpDingReceiverstatusListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.confirmed_status = None
        self.ding_id = None
        self.page_no = None
        self.page_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.corp.ding.receiverstatus.list'
