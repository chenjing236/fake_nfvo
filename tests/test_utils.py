#! /usr/bin/python
# coding:utf-8
import socket
import json
from webob import Request
from faked_nfvo.api.schemas import tokens
from faked_nfvo.requests.rest_client import RestClient


def get_token_from_nfvo(username=None, password=None,
                        VimId='81f1d9d0-ca13-4eea-a4ce-9bd89a50c9d1',
                        scheme="http", server_ip=None, server_port=None,
                        qType="vim", method="POST"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    if server_ip is None:
        server_ip = s.getsockname()[0]
    if server_port is None:
        server_port = 9131

    req = Request.blank(
        "%s://%s:%s/v1/%sTokens" % (scheme, server_ip, server_port, qType))
    req.method = method
    req.headers = {
        'X-Auth-Username': username,
        "X-Auth-Password": password
    }
    req.body = json.dumps({
        "VimId": VimId
    })
    res = req.get_response()
    body = json.loads(res.body)
    RestClient.validate_response(tokens.token_for_nfvo, res, body)
    return res
