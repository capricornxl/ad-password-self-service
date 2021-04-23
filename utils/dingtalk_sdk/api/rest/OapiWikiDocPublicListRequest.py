"""
Created by auto_sdk on 2020.10.16
"""
from api.base import RestApi


class OapiWikiDocPublicListRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.cursor = None
        self.group_id = None
        self.size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.wiki.doc.public.list'
