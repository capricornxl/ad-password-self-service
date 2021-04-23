"""
Created by auto_sdk on 2020.07.16
"""
from api.base import RestApi


class OapiRhinoMosExecTrackBindRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.entities = None
        self.entity_type = None
        self.order_id = None
        self.tenant_id = None
        self.track_id = None
        self.track_type = None
        self.userid = None
        self.workstation_code = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.rhino.mos.exec.track.bind'
