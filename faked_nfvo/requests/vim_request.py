#! /usr/bin/python
# coding:utf-8

__author__ = 'zhangyafeng'

import json
import logging

from webob import Request
from faked_nfvo.api.schemas import vim_cm
from rest_client import RestClient
import request_utils
from faked_nfvo.api.schemas import vim_alarm
from faked_nfvo.api.schemas import vim_pm

base_url = request_utils.get_base_url(server_type="vim")
HEADERS = request_utils.get_header()


LOG = logging.getLogger(__name__)


def listActiveAlarms():
    req = Request.blank("%s/v1/vimFm/activeAlarms" % base_url)
    req.method = "GET"
    req.headers = HEADERS
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "vim"})
    print "--------------------------------"
    print req
    print "--------------------------------"
    res = req.get_response()
    print "++++++++++++++++++++++++++++++++"
    print res
    print "++++++++++++++++++++++++++++++++"
    LOG.info(res)
    RestClient.validate_response(vim_alarm.list_active_alarms, res, res.body)
    return res


def listHistoryAlarms():
    req = Request.blank("%s/v1/vimFm/hisAlarms" % base_url)
    req.method = "GET"
    req.headers = HEADERS
    req.body = json.dumps(
        {"NfvoId": "BJ-NFVO-1", "qType": "vim", "StartSeq": 230})
    print "--------------------------------"
    print req
    print "--------------------------------"
    res = req.get_response()
    print "++++++++++++++++++++++++++++++++"
    print res
    print "++++++++++++++++++++++++++++++++"
    LOG.info(res)
    RestClient.validate_response(vim_alarm.list_history_alarms, res, res.body)
    return res


def list_res_details():
    req = Request.blank("%s/v1/vimCm?NfvoId=BJ-NFVO-1&qType=VIM" % base_url)
    req.method = "GET"
    req.headers = HEADERS
    print "--------------------------------"
    print req
    print "--------------------------------"
    resp = req.get_response()
    print "++++++++++++++++++++++++++++++++"
    print resp
    print "++++++++++++++++++++++++++++++++"
    LOG.info(resp)
    body = json.loads(resp.body)
    RestClient.validate_response(vim_cm.list_res_details_response, resp, body)
    return resp


def list_history_metrics():
    req = Request.blank("%s/v1/vimPm/hisMetrics?NfvoId=BJ-NFVO-1&qType=vim" % base_url)
    req.method = "GET"
    req.headers = HEADERS
    print "--------------------------------"
    print req
    print "--------------------------------"
    resp = req.get_response()
    LOG.info(resp)
    print "++++++++++++++++++++++++++++++++"
    print resp
    print "++++++++++++++++++++++++++++++++"
    RestClient.validate_response(vim_pm.list_history_metrics_response, resp,
                                 resp.body)
    return resp
