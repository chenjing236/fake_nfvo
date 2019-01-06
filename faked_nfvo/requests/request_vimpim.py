#!/usr/bin/env python
# coding=utf-8

import json
import logging
import argparse
from ConfigParser import SafeConfigParser
from webob import Request
from rest_client import RestClient
from faked_nfvo.api.schemas import vimJobs as schema_vimJobs
from faked_nfvo.api.schemas import vimJobs as schema_pimJobs
from faked_nfvo.requests import request_utils

content_type_headers = 'application/json; charset=UTF-8'
pim_token = request_utils.get_pim_token('admin', 'admin')
LOG = logging.getLogger(__name__)
LOG_FILE_NAME = 'faked_nfvo.log'
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d %(levelname)s  %(message)s'


class RequestVIMPIM:
    def __init__(self, vimhostip, vimport, pimhostip, pimport, scheme="http"):
        self.scheme = scheme
        self.vimhostip = vimhostip
        self.vimport = vimport
        self.pimhostip = pimhostip
        self.pimport = pimport
        self.cmds = {
            "vimlistsubscriptions": self.vim_ListSubscriptions,
            "vimcreatesubscription": self.vim_CreateSubscription,
            "vimdeletesubscription": self.vim_DeleteSubscription,
            "pimlistsubscriptions": self.pim_ListSubscriptions,
            "pimcreatesubscritpion": self.pim_CreateSubscription,
            "pimdeletesubscription": self.pim_DeleteSubscription
        }
        parser = SafeConfigParser()
        parser.read("/etc/faked_nfvo/cfg.ini")
        self.cert_path = parser.get('DEFAULT', 'CERT')
        self.nfvo_server_ip = parser.get('DEFAULT', 'nfvo_server_ip')
        self.nfvo_server_port = parser.get('DEFAULT', 'nfvo_port')

    def vim_ListSubscriptions(self):
        '''
        Send a request for listing subscriptions to VIM
        '''
        req = Request.blank(
            '%s://%s:%s/v1/vimJobs?NfvoId=BJ-NFVO-1&qType=vim&subtype[]=vimCm&subtype[]=vimPm&subtype[]=vimFm'
            % (self.scheme, self.vimhostip, self.vimport))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = vim_token
        req.method = 'GET'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = json.loads(resp.body)
        RestClient.validate_response(schema_vimJobs.listsubscriptions, resp,
                                     body)
        return resp

    def pim_ListSubscriptions(self):
        '''
        Send a request for listing subscriptions to PIM
        '''
        req = Request.blank('%s://%s:%s/v1/pimJobs?NfvoId=BJ-NFVO-1&qType=pim'
                            % (self.scheme, self.pimhostip, self.pimport))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = pim_token
        req.method = 'GET'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = json.loads(resp.body)
        RestClient.validate_response(schema_pimJobs.listsubscriptions, resp,
                                     body)
        return resp

    def pim_ListSubscriptions_with_curl(self):
        cmd = "curl -X GET -k -v '%s://%s:%s/v1/pimJobs?NfvoId=BJ-NFVO-0&qType=pim' " \
              "-H 'Content-Type:application/json;charset:UTF-8' -H 'X-Auth-Token:%s'" % \
              (self.scheme, self.pimhostip, self.pimport, pim_token)
        print cmd
        child = subprocess.call(cmd, shell=True)
    
    def vim_CreateSubscription(self, nfvo_id="BJ-NFVO-1", period=15, hb_cm=30, hb_fm=30):
        '''
        Send a request for creating subscriptions to VIM
        '''
        req = Request.blank('%s://%s:%s/v1/vimJobs' % (
            self.scheme, self.vimhostip, self.vimport))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = vim_token
        req.body = json.dumps({
            "NfvoId": nfvo_id,
            "Username": "admin",
            "Password": "admin",
            "IdentityUri": "http://%s:%s/v1/vimTokens"
                           % (self.nfvo_server_ip, self.nfvo_server_port ),
            "subType": "vim",
            "Period": period,
            "HeartbeatCm": hb_cm,
            "HeartbeatFm": hb_fm
        })
        req.method = 'POST'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = json.loads(resp.body)
        RestClient.validate_response(schema_vimJobs.createsubscription, resp,
                                     body)
        return resp

    def pim_CreateSubscription(self):
        '''
        Send a request for creating subscriptions to PIM
        '''
        req = Request.blank('%s://%s:%s/v1/pimJobs' % (
            self.scheme, self.pimhostip, self.pimport))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = pim_token
        req.body = json.dumps({
            "NfvoId": "BJ-NFVO-1",
            "Username": "Guest",
            "Password": "Guest",
            "IdentityUri": "http://%s/pimTokens" % self.nfvo_server_ip,
            "subType": "pim",
            "Period": "15",
            "Heartbeat": "30"
        })
        req.method = 'POST'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = json.loads(resp.body)
        RestClient.validate_response(schema_pimJobs.createsubscription, resp,
                                     body)
        return resp

    def pim_CreateSubscription_with_curl(self, NfvoId, user, password,
                                         identity, subtype, period, heartbeat):
        '''
        Send a request for creating subscriptions to PIM
        '''
        cmd = "curl -X POST -k -v %s://%s:%s/v1/pimJobs " \
              "-H 'Content-Type:application/json;charset:UTF-8' -H 'X-Auth-Token:%s' " \
              "-d '{\"NfvoId\":\"%s\", \"Username\":\"%s\", \"Password\":\"%s\", \"IdentityUri\":\"%s\", \"subType\":\"%s\", \"Period\":%s, \"Heartbeat\":%s}'" % \
              (self.scheme, self.pimhostip, self.pimport, pim_token, NfvoId,
               user, password, identity, subtype, period, heartbeat)
        print cmd
        child = subprocess.call(cmd, shell=True)

    def vim_DeleteSubscription(self, nfvo_id):
        '''
        Send a request for deleting subscriptions to VIM
        '''
        req = Request.blank(
            '%s://%s:%s/v1/vimJobs?NfvoId=%s&qType=vim&subType[]=vimCM'
            % (self.scheme, self.vimhostip, self.vimport, nfvo_id))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = vim_token
        req.method = 'DELETE'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = None
        if resp.body:
            body = json.loads(resp.body)
        RestClient.validate_response(schema_vimJobs.deletesubscription,
                                     resp, body)
        return resp

    def pim_DeleteSubscription(self):
        '''
        Send a request for deleting subscriptions to PIM
        '''
        req = Request.blank('%s://%s:%s/v1/pimJobs/BJ-NFVO-1?subType=pim'
                            % (self.scheme, self.pimhostip, self.pimport))
        req.headers['Content-Type'] = content_type_headers
        req.headers['X-Auth-Token'] = pim_token
        req.method = 'DELETE'
        print "--------------------------------"
        print req
        print "--------------------------------"
        resp = req.get_response()
        print "++++++++++++++++++++++++++++++++"
        print resp
        print "++++++++++++++++++++++++++++++++"
        LOG.info(resp)
        body = None
        if resp.body:
            body = json.loads(resp.body)
        RestClient.validate_response(schema_pimJobs.deletesubscription, resp,
                                     body)
        return resp

    def pim_DeleteSubscription_with_curl(self, nfvoid, subtype):
        '''
        Send a request for deleting subscriptions to PIM
        '''
        cmd = "curl -X DELETE -k -v %s://%s:%s/v1/pimJobs/%s?subType=%s " \
              "-H 'Content-Type:application/json;charset:UTF-8' -H 'X-Auth-Token:%s'" % \
              (self.scheme, self.pimhostip, self.pimport, nfvoid, subtype, pim_token)
        print cmd
        child = subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     "This script can request VIM/PIM and verify the responses.")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose mode')
    parser.add_argument('--vimlistsubscriptions', action='store_true',
                        help='send a request for listing subscriptions to VIM')
    parser.add_argument('--vimcreatesubscription', action='store_true',
                        help='send a request for creating subscripting to VIM')
    parser.add_argument('--vimdeletesubscription', action='store_true',
                        help='send a request for deleting subscription to VIM')
    parser.add_argument('--pimlistsubscriptions', action='store_true',
                        help='send a request for listing subscriptions to PIM')
    parser.add_argument('--pimcreatesubscritpion', action='store_true',
                        help='send a request for creating subscripting to PIM')
    parser.add_argument('--pimdeletesubscription', action='store_true',
                        help='send a request for deleting subscription) to PIM')
    args = parser.parse_args()
    req = RequestVIMPIM('10.100.3.235', '9131', '10.100.3.235', '9131')
    for cmd, status in vars(args).items():
        if status:
            req.cmds[cmd]()
