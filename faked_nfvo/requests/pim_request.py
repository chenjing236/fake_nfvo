#! /usr/bin/python
# coding:utf-8
__author__ = 'zhangyafeng'

import json
import logging
from webob import Request
from rest_client import RestClient
import request_utils
from faked_nfvo.api.schemas import pim_cm
from faked_nfvo.api.schemas import pim_alarm

base_url = request_utils.get_base_url(server_type="pim")
headers = {"Content-Type": "application/json;charset=UTF-8",
           "X-Auth-Token": request_utils.get_token(server_type="pim")}

LOG = logging.getLogger(__name__)


def listResDetails():
    req = Request.blank("%s/v1/pimCm" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_res_details, res, body)
    return res


def listChassisList():
    req = Request.blank("%s/v1/pimCm/Chassis" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_chassis_list, res, body)
    return res


def listChassisDetails():
    req = Request.blank("%s/v1/pimCm/Chassis/1U" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_chassis_details, res, body)
    return res


def listSystemList():
    req = Request.blank("%s/v1/pimCm/Systems" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_system_list, res, body)
    return res


def listSystemDetails():
    req = Request.blank("%s/v1/pimCm/Systems/437XR1138R2" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_system_details, res, body)
    return res


def listDiskArrayChassisList():
    req = Request.blank("%s/v1/pimCm/DiskArrayChassis" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_disk_array_chassis_list, res,
                                 body)
    return res


def listDiskArrayChassisDetails():
    req = Request.blank("%s/v1/pimCm/DiskArrayChassis/1U" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_disk_array_chassis_details, res,
                                 body)
    return res


def listDiskArraySystemList():
    req = Request.blank("%s/v1/pimCm/DiskArraySystems" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_disk_array_system_list, res,
                                 body)
    return res


def listDiskArraySystemDetails():
    req = Request.blank(
        "%s/v1/pimCm/DiskArraySystems/437XR1138R2" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_disk_array_system_details, res,
                                 body)
    return res


def listHistoryMetrics():
    req = Request.blank("%s/v1/pimPm/hisMetrics" % base_url)
    req.method = "GET"
    req.headers = headers
    req.body = json.dumps({"NfvoId": "BJ-NFVO-1", "qType": "pim",
                           "StartTime": "2017-06-01T00:00:00Z"})
    res = req.get_response()
    LOG.info(res)
    body = json.loads(res.body)
    RestClient.validate_response(pim_cm.list_history_metrics, res, body)
    return res


def list_active_alarms():
    req = Request.blank("%s/v1/pimFm/activeAlarms?NfvoId=BJ-NFVO-1&qType=pim"
                        % base_url)
    req.method = "GET"
    req.headers = headers
    resp = req.get_response()
    LOG.info(resp)
    body = json.loads(resp.body)
    RestClient.validate_response(pim_alarm.list_active_alarms, resp, body)
    return resp


def list_history_alarms():
    req = Request.blank("%s/v1/pimFm/hisAlarms?NfvoId=BJ-NFVO-1&qType=pim"
                        % base_url)
    req.method = "GET"
    req.headers = headers
    resp = req.get_response()
    LOG.info(resp)
    body = json.loads(resp.body)
    RestClient.validate_response(pim_alarm.list_history_alarms, resp, body)
    return resp
