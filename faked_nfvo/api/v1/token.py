import json
import logging
from webob import Response
from ConfigParser import SafeConfigParser

from faked_nfvo.api import validation
from faked_nfvo.api.schemas import tokens
from faked_nfvo.token_mgmt import TokenMgmt
from faked_nfvo.api import api_utils

LOG = logging.getLogger(__name__)

parser = SafeConfigParser()
parser.read("/etc/faked_nfvo/cfg.ini")
server_ip = parser.get('DEFAULT', 'nfvo_server_ip')
server_port = parser.get('DEFAULT', 'nfvo_port')

class VIMTokenController(object):
    @validation.schema(request_body_schema=tokens.get_token)
    def get_token(self, req, body):
        r = Response()
        r.status = "201"
        cached_token_path = api_utils.get_cached_token_path()
        token_mgmt = TokenMgmt(cached_token_path)
        token = token_mgmt.get_token()
        issued = token_mgmt.get_issued_time(token)
        r.body = json.dumps(
            {"Token": token_mgmt.get_token_id(),
             "IssuedAt": issued,
             "ExpiresAt": token_mgmt.get_expires_time(issued),
             "CallBackUris": [{"UriType": "vimCm",
                               "CallBackUri": "http://%s:%s/v1/vimCm" % (server_ip, server_port)},
                              {"UriType": "vimPm",
                               "CallBackUri": "http://%s:%s/v1/vimPm" % (server_ip, server_port)},
                              {"UriType": "vimFm",
                               "CallBackUri": "http://%s:%s/v1/vimFm" % (server_ip, server_port)}]
             }
        )
        return r


class PIMTokenController(object):
    @validation.schema(request_body_schema=tokens.get_token)
    def get_token(self, req, body):
        r = Response()
        r.status = "201"
        cached_token_path = api_utils.get_cached_token_path()
        token_mgmt = TokenMgmt(cached_token_path)
        token = token_mgmt.get_token()
        issued = token_mgmt.get_issued_time(token)
        r.body = json.dumps(
            {"Token": token_mgmt.get_token_id(),
             "IssuedAt": issued,
             "ExpiresAt": token_mgmt.get_expires_time(issued),
             "CallBackUris": [{"UriType": "pimCm",
                               "CallBackUri": "https://%s/pimCm" % server_ip},
                              {"UriType": "pimPm",
                               "CallBackUri": "https://%s/pimPm" % server_ip},
                              {"UriType": "pimFm",
                               "CallBackUri": "https://%s/pimFm" % server_ip}]
             }
        )
        return r
