#! /usr/bin/python
# coding:utf-8

import unittest
import os
import time
from datetime import datetime
import test_utils
import utils
from faked_nfvo.requests import request_utils
from faked_nfvo.requests import vim_request
from faked_nfvo.requests.request_vimpim import RequestVIMPIM

conf_util = request_utils.ConfigUtil()
vim_host = conf_util.get("host", "vim")
vim_port = conf_util.get("port", "vim")
pim_host = conf_util.get("host", "pim")
pim_port = conf_util.get("port", "pim")

DEBUG = True

resp_kword_map = {
    "vimcreatesubscription": "get_token",
    "pushalarms": "get_push_info",
    "pushheartbeat": "push_info"
}

nfvoip = "192.168.58.235"
nfvoport = "9131"

host_username = "root"
host_ip = "10.100.64.17"
envfile = "/root/openrc"

nic = "net-name=share_net"
imagename = "centos"
flavorname = "2-2048-20"
vmname = "VIMScenario_" + utils.generate_random_string(6)

vimcreatesubscription_timeout = 30
pushalarms_timeout = 30
pushheartbeat_timeout = 30
waitvimready_secs = 60


class VIMFMPushAlarmTest(unittest.TestCase):
    def setUp(self):
        self.request = RequestVIMPIM(vim_host, vim_port, pim_host, pim_port)

    @unittest.skip("testPushAlarms ... skip")
    def testPushAlarms(self):
        """
            case16:VIM FM push alarms mechanism
        """
        print("%s ... %s" % ("testPushAlarms", "start"))
        # 1. CreateResSubcriptions(NFVO->VIM), only for fm
        vimcreatesubscription_timestamp = datetime.now()
        self.request.vim_CreateSubscription(period=None, heartbeatcm=None,
                                            heartbeatfm="30")

        # 2. AuthForPushData(VIM->NFVO)
        if DEBUG:
            test_utils.get_token_from_nfvo(qType="vim")

        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           vimcreatesubscription_timeout,
                                           resp_kword_map[
                                               "vimcreatesubscription"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request info in faked-api.log in 30 seconds.")

        # 3. Simulate kernel panic for VM
        print("- 3 - Simulate kernel panic for VM")
        pushalarms_timestamp = datetime.now()
        pushheartbeat_timestamp = datetime.now()
        # create a vm with a user-data that raise a kernel panic
        os.system(
            'ssh %s@%s \'echo "#!/bin/bash" > /root/user.sh && echo "sleep %s" >> /root/user.sh && echo "echo 1 > /proc/sys/kernel/sysrq; echo c | tee /proc/sysrq-trigger" >> /root/user.sh\'' % (
                host_username, host_ip, waitvimready_secs))
        os.system(
            'ssh %s@%s "source %s && nova boot --image %s --flavor %s --nic %s %s --user-data /root/user.sh"' % (
                host_username, host_ip, envfile, imagename, flavorname, nic,
                vmname))
        print("Waiting %s seconds for simulating kernel panic ..." % (
            waitvimready_secs * 5))
        time.sleep(waitvimready_secs * 5)

        # 4. PushAlarms(VIM->NFVO)
        print("- 4 - PushAlarms(VIM->NFVO)")
        time.sleep(1)
        if DEBUG:
            os.system(
                'curl -X PUT http://%s:%s/v1/vimFm -d \'{ "Version": "1.0", "VimId": "123", "SrcType": "vim", "MsgType": "vimFmAlarm", "AlarmList": [ { "alarmTitle": "Server1 Down!", "alarmStatus": 1, "alarmType": "vm", "origSeverity": 1, "eventTime": "2016-06-16T21:12:54Z", "alarmId": "200", "msgSeq": 230, "specificProblemID": "0126.37", "specificProblem": "Kernel Panic", "neUID": "ed8qe", "neName": "Server1", "neType": "vm", "objectUID": "ed8", "objectName": "Server1", "objectType": "vm", "locationInfo": "Compute-1", "addInfo": "", "PVFlag": "vim"  }  ], "CurrentBatch": 1, "TotalBatches": 1 }\'' % (
                    nfvoip, nfvoport))
        result = utils.wait_response_inlog(pushalarms_timestamp,
                                           pushalarms_timeout,
                                           resp_kword_map["pushalarms"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")

        # 5. Kernal panic VM recovery


        # 6. PushAlarms(VIM->NFVO)
        print("- 6 - PushAlarms(VIM->NFVO)")
        time.sleep(1)
        if DEBUG:
            os.system(
                'curl -X PUT http://%s:%s/v1/vimFm -d \'{ "Version": "1.0", "VimId": "123", "SrcType": "vim", "MsgType": "vimFmAlarm", "AlarmList": [ { "alarmTitle": "Server1 Down!", "alarmStatus": 1, "alarmType": "vm", "origSeverity": 1, "eventTime": "2016-06-16T21:12:54Z", "alarmId": "200", "msgSeq": 230, "specificProblemID": "0126.37", "specificProblem": "Kernel Panic", "neUID": "ed8qe", "neName": "Server1", "neType": "vm", "objectUID": "ed8", "objectName": "Server1", "objectType": "vm", "locationInfo": "Compute-1", "addInfo": "", "PVFlag": "vim"  }  ], "CurrentBatch": 1, "TotalBatches": 1 }\'' % (
                    nfvoip, nfvoport))
        result = utils.wait_response_inlog(pushalarms_timestamp,
                                           pushalarms_timeout,
                                           resp_kword_map["pushalarms"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")

        # 7. DeleteResSubcriptions(NFVO->VIM)
        self.request.vim_DeleteSubscription()

        print("%s ... %s" % ("testPushAlarms", "finished"))

    @unittest.skip("testAlarmConcurrencyTest ... skip")
    def testAlarmConcurrencyTest(self):
        """
            case17	VIM FM concurrency mechanism
        :return: 
        """
        print("%s ... %s" % ("testAlarmConcurrencyTest", "start"))
        # 1. CreateResSubcriptions(NFVO->VIM), only for fm
        vimcreatesubscription_timestamp = datetime.now()
        self.request.vim_CreateSubscription()

        # 2. AuthForPushData(VIM->NFVO)
        if DEBUG:
            test_utils.get_token_from_nfvo(qType="vim")

        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           vimcreatesubscription_timeout,
                                           resp_kword_map[
                                               "vimcreatesubscription"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request info in faked-api.log in 30 seconds.")

        # 3. Simulate kernel panic for VM
        print("- 3 - Simulate kernel panic for VM")
        pushalarms_timestamp = datetime.now()
        pushheartbeat_timestamp = datetime.now()
        # create a vm with a user-data that raise a kernel panic
        os.system(
            'ssh %s@%s \'echo "#!/bin/bash" > /root/user.sh && echo "sleep %s" >> /root/user.sh && echo "echo 1 > /proc/sys/kernel/sysrq; echo c | tee /proc/sysrq-trigger" >> /root/user.sh\'' % (
                host_username, host_ip, waitvimready_secs))
        os.system(
            'ssh %s@%s "source %s && nova boot --image %s --flavor %s --nic %s %s --user-data /root/user.sh"' % (
                host_username, host_ip, envfile, imagename, flavorname, nic,
                vmname))
        print("Waiting %s seconds for simulating kernel panic ..." % (
            waitvimready_secs * 5))
        time.sleep(waitvimready_secs * 5)

        # ListHistoryAlarms(NFVO->VIM)

        #

        # 5. DeleteResSubcriptions(NFVO->VIM)
        self.request.vim_DeleteSubscription()
        print("%s ... %s" % ("testAlarmConcurrencyTest", "finished"))

    @unittest.skip("Query alarms info when there is no alarm ... skip")
    def testQueryAlarmsInfoWhenNoAlarmExist(self):
        """
            case18	Query alarms info when there is no alarm
        :return: 
        """
        print("%s ... %s" % ("testQueryAlarmsInfoWhenNoAlarmExist", "start"))
        # 1. CreateResSubcriptions(NFVO->VIM), only for fm
        vimcreatesubscription_timestamp = datetime.now()
        self.request.vim_CreateSubscription()

        # 2. AuthForPushData(VIM->NFVO)
        if DEBUG:
            test_utils.get_token_from_nfvo(qType="vim")

        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           vimcreatesubscription_timeout,
                                           resp_kword_map[
                                               "vimcreatesubscription"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request info in faked-api.log in 30 seconds.")

        # 3. ListActiveAlarms(NFVO->VIM)
        vim_request.listActiveAlarms()

        # 4. ListHistoryAlarms(NFVO->VIM)
        vim_request.listHistoryAlarms()

        # 5. DeleteResSubcriptions(NFVO->VIM)
        self.request.vim_DeleteSubscription()
        print("%s ... %s" % ("testQueryAlarmsInfoWhenNoAlarmExist", "finished"))

    @unittest.skip("VIM FM data storage time ... skip ")
    def testQueryAlarmsForMore(self):
        """
            case19	VIM FM data storage time
        :return: 
        """
        print("%s ... %s" % ("testQueryAlarmsForMore", "start"))
        # 1. ListActiveAlarms(NFVO->VIM)
        vim_request.listActiveAlarms()

        # 2. ListHistoryAlarms(NFVO->VIM)
        vim_request.listHistoryAlarms()

        print("%s ... %s" % ("testQueryAlarmsForMore", "finished"))

    @unittest.skip("VIM FM retransmission mechanism ... skip ")
    def testVIMFMRetransmission(self):
        """
            case 15:VIM FM retransmission mechanism
        :return: 
        """


if __name__ == '__main__':
    unittest.main()
