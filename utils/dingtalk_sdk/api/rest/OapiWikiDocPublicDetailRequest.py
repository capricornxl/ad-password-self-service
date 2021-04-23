"""
Created by auto_sdk on 2020.10.16
"""
from api.base import RestApi


class OapiWikiDocPublicDetailRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agentid = None
        self.doc_id = None
        self.group_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.wiki.doc.public.detail'
