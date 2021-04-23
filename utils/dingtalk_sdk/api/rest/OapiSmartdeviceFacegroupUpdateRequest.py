"""
Created by auto_sdk on 2019.07.01
"""
from api.base import RestApi


class OapiSmartdeviceFacegroupUpdateRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.bg_img_url = None
        self.biz_id = None
        self.end_time = None
        self.greeting_msg = None
        self.start_time = None
        self.status = None
        self.title = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.smartdevice.facegroup.update'
