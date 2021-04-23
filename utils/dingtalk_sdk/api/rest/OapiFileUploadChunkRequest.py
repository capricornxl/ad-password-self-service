"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiFileUploadChunkRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.chunk_sequence = None
        self.file = None
        self.upload_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.file.upload.chunk'

    def getMultipartParas(self):
        return ['file']
