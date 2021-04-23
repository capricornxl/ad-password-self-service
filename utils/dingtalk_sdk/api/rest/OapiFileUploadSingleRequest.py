"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiFileUploadSingleRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.file = None
        self.file_size = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.file.upload.single'

    def getMultipartParas(self):
        return ['file']
