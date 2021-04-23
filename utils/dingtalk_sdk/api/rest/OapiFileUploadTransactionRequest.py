"""
Created by auto_sdk on 2018.07.25
"""
from api.base import RestApi


class OapiFileUploadTransactionRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.agent_id = None
        self.chunk_numbers = None
        self.file_size = None
        self.upload_id = None

    def getHttpMethod(self):
        return 'GET'

    def getapiname(self):
        return 'dingtalk.oapi.file.upload.transaction'
