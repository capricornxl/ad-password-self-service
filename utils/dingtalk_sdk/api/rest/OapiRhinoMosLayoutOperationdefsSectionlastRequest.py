"""
Created by auto_sdk on 2020.04.08
"""
from api.base import RestApi


class OapiRhinoMosLayoutOperationdefsSectionlastRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.flow_version = None
        self.need_assign_info = None
        self.order_id = None
        self.section_code = None
        self.tenant_id = None
        self.tmp_save = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.layout.operationdefs.sectionlast'
