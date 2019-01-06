#!/usr/bin/env python
# coding=utf-8


import logging


supported_methods = ['get', 'post']


LOG = logging.getLogger(__name__)


def verify(req):
    if req.method.lower() not in supported_methods:
        LOG.error('')
    if req.body.get("NfvoId") and req.body.get("qType"):
        return True
    if (body.get("NfvoId") and body.get("IdentityUri")
        and body.get("subType") and body.get("Period")
        and body.get("Heartbeat")):
        return True


def response():
    return {
        "NfvoId": "BJ-NFVO-1",
        "IdentityUri": "https://192.168.112.100/tokens",
        "subType": "vim",
        "Period": 15,
        "Heartbeat": 30
    }
