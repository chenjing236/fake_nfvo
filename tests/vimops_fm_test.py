import utils
import os
import time
from datetime import datetime
from faked_nfvo.requests.request_vimpim import RequestVIMPIM
from faked_nfvo.requests import vim_request
from faked_nfvo.requests import request_utils

'''
PLEASE NOTE:
1. Provide VIM host ip and port
2. Provide the env file for authentication
3. Provide the resource to create an instance
'''

resp_kword_map = {
    "vimcreatesubscription": "get_token",
    "pushalarms": "get_push_info",
    "pushheartbeat": "push_info"
}

if __name__ == '__main__':
    debug = False

    # host_username = "root"
    # host_ip = "10.100.64.17"
    envfile = "/root/openrc"

    nic = "net-name=share_net"
    imagename = "centos"
    flavorname = "2-2048-20"
    vmname = "VIMScenario_" + utils.generate_random_string(6)

    vimcreatesubscription_timeout = 30
    pushalarms_timeout = 60
    pushheartbeat_timeout = 30
    waitvimready_secs = 60

    req = RequestVIMPIM(request_utils.get_host('vim'),
                        request_utils.get_port('vim'),
                        request_utils.get_host('pim'),
                        request_utils.get_port('pim'))

    # 1. CreateResSubcriptions(NFVO->VIM)
    print("- 1 - CreateResSubcriptions(NFVO->VIM)")
    vimcreatesubscription_timestamp = datetime.now()
    nfvo_id = "cloudtest_" + utils.generate_random_string(6)
    req.vim_CreateSubscription(nfvo_id)

    # 2. AuthForPushData(VIM->NFVO)
    print("- 2 - AuthForPushData(VIM->NFVO)")
    time.sleep(1)
    nfvo_ip, nfvo_port = utils.get_nfvo_server_ip_port()
    if debug:
        os.system('curl -X POST http://%s:%s/v1/vimTokens -d \'{"VimId": "123456789012345678901234567890123456"}\''
                  % (nfvo_ip, nfvo_port))
    result = utils.wait_response_inlog(vimcreatesubscription_timestamp, vimcreatesubscription_timeout, 
                           resp_kword_map["vimcreatesubscription"], True) 
    if result['resp'] and result['validated']:
        print("Got the request and it was validated.")

    # 3. Simulate kernel panic for VM
    print("- 3 - Simulate kernel panic for VM")
    pushalarms_timestamp = datetime.now()
    pushheartbeat_timestamp = datetime.now()
    os.system("source ~/openrc && ceilometer alarm-threshold-create --name cpu_high130 "
              "--description 'instance running hot'  --meter-name cpu_util  "
              "--threshold 10.0 --comparison-operator ne  --statistic avg "
              "--period 60 --evaluation-periods 3  "
              "--query resource_id=915dac10-b534-40e5-b5d0-1bbb8ed01f29")
    #create a vm with a user-data that raise a kernel panic
    # os.system('ssh %s@%s \'echo "#!/bin/bash" > /root/user.sh && echo "sleep %s" >> /root/user.sh && echo "echo 1 > /proc/sys/kernel/sysrq; echo c | tee /proc/sysrq-trigger" >> /root/user.sh\'' % (host_username, host_ip, waitvimready_secs ))
    # os.system('ssh %s@%s "source %s && nova boot --image %s --flavor %s --nic %s %s --user-data /root/user.sh"' % (host_username, host_ip, envfile, imagename, flavorname, nic, vmname))
    print("Waiting %s seconds for simulating kernel panic ..." % (waitvimready_secs*5))
    time.sleep(waitvimready_secs*5)

    # 4. PushAlarms(VIM->NFVO)
    print("- 4 - PushAlarms(VIM->NFVO)")
    time.sleep(1)
    if debug:
        os.system('curl -X PUT http://%s:%s/v1/vimFm -d \'{ "Version": "1.0", "VimId": "123", "SrcType": "vim", "MsgType": "vimFmAlarm", "AlarmList": [ { "alarmTitle": "Server1 Down!", "alarmStatus": 1, "alarmType": "vm", "origSeverity": 1, "eventTime": "2016-06-16T21:12:54Z", "alarmId": "200", "msgSeq": 230, "specificProblemID": "0126.37", "specificProblem": "Kernel Panic", "neUID": "ed8qe", "neName": "Server1", "neType": "vm", "objectUID": "ed8", "objectName": "Server1", "objectType": "vm", "locationInfo": "Compute-1", "addInfo": "", "PVFlag": "vim"  }  ], "CurrentBatch": 1, "TotalBatches": 1 }\''
                  % (nfvo_ip, nfvo_port))
    result = utils.wait_response_inlog(pushalarms_timestamp, pushalarms_timeout, 
                           resp_kword_map["pushalarms"], True) 
    if result['resp'] and result['validated']:
        print("Got the request and it was validated.")

    # 5. PushFmHeartbeat(VIM->NFVO)
    print("- 5 - PushFmHeartbeat(VIM->NFVO)")
    time.sleep(1)
    if debug:
        os.system('curl -X PUT http://%s:%s/v1/vimCm -d \'{"Version": "1.0", "VimId": "81f1d9d0-ca13-4eea-a4ce-9bd89a50c9d1", "SrcType": "vpim", "MsgType": "vimCmHeartbeat"}\'' % (nfvo_ip, nfvo_port))
    result = utils.wait_response_inlog(pushheartbeat_timestamp, pushheartbeat_timeout, 
                           resp_kword_map["pushheartbeat"], True) 
    if result['resp'] and result['validated']:
        print("Got the request and it was validated.")

    # 6. ListActiveAlarms(NFVO->VIM)
    print("- 6 - ListActiveAlarms(NFVO->VIM)")
    vim_request.listActiveAlarms()
    
    # 7. ListHistoryAlarms(NFVO->VIM)
    print("- 7 - ListHistoryAlarms(NFVO->VIM)")
    vim_request.listHistoryAlarms()
    
    # 8. DeleteResSubcriptions(NFVO->VIM)
    print("- 8 - DeleteResSubcriptions(NFVO->VIM)")
    req.vim_DeleteSubscription(nfvo_id)


    # time.sleep(10)
    # os.system('source %s && nova delete %s' % (envfile, vmname))
    # os.system('ssh %s@%s "source %s && nova delete %s"' % (host_username, host_ip, envfile, vmname))

