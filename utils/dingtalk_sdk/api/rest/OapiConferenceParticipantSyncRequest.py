"""
Created by auto_sdk on 2019.07.03
"""
from api.base import RestApi


class OapiConferenceParticipantSyncRequest(RestApi):
    def __init__(self, url=None):
        RestApi.__init__(self, url)
        self.batch_id = None
        self.batch_index = None
        self.conference_id = None
        self.is_finished = None
        self.participant_userid_list = None
        self.userid = None

    def getHttpMethod(self):
        return 'POST'

    def getapiname(self):
        return 'dingtalk.oapi.conference.participant.sync'
