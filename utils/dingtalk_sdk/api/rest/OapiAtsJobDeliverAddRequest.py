"""
Created by auto_sdk on 2020.08.04
"""
from api.base import RestApi


class OapiAtsJobDeliverAddRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.biz_code = None
        self.deliver_channel = None
        self.deliver_msg = None
        self.deliver_outer_id = None
        self.deliver_status = None
        self.job_id = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.ats.job.deliver.add'
