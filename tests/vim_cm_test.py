#!/usr/bin/env python

import unittest
import json
import jsonschema
import os
import exceptions
import time
from datetime import datetime

from faked_nfvo.requests import vim_request
from faked_nfvo.requests import request_utils
from faked_nfvo.requests.request_vimpim import RequestVIMPIM
from faked_nfvo.api.schemas import vim_cm
from faked_nfvo.requests import rest_client
import utils

resp_kword_map = {
    "vimcreatesubscription": "get_token",
    "pushalarms": "get_push_info",
    "pushheartbeat": "push_info"
}


class VimCmTest(unittest.TestCase):
    def setUp(self):
        self.req = RequestVIMPIM(request_utils.get_host('vim'),
                                 request_utils.get_port('vim'),
                                 request_utils.get_host('pim'),
                                 request_utils.get_port('pim'))

    def tearDown(self):
        cmd = "source ~/openrc && nova delete cloudtest_vim_cm"
        os.system(cmd)
        cmd = "openstack aggregate remove host cloudtest node-3.domain.tld"
        os.system(cmd)
        self.req.vim_DeleteSubscription()

    def get_res_details(self, res_file_path):
        print "Try to list vim_cm resource details!"
        resp = vim_request.list_res_details()
        print resp
        body = json.loads(resp.body)
        res_file_uri = body.get('FileUri')
        print "Try to download resource file from uri: %s" \
              % res_file_uri
        # res_file_uri = "http://10.100.109.58/cloudtest_results/test_vim_cm.gz"
        os.system("wget -c %s" % res_file_uri)
        cmd = "tar -xvf %s > filename" % res_file_uri.split('/')[-1]
        os.system(cmd)
        with open("./filename") as f:
            filename = f.read()
        cmd = "mv %s %s" % (filename.split('\n')[0], res_file_path)
        os.system(cmd)

        with open(res_file_path) as f:
            res_details = f.read()
        res_details_json = json.loads(res_details)
        try:
            jsonschema.validate(res_details_json, vim_cm.res_details,
                                cls=rest_client.JSONSCHEMA_VALIDATOR,
                                format_checker=rest_client.FORMAT_CHECKER)
        except jsonschema.ValidationError as ex:
            msg = ("Json schema is invalid (%s)" % ex)
            raise exceptions.Exception(msg)

        return res_details_json

    def test_VIMops_cm_scenario(self):
        debug = True
        res_file_path_before = "./res_file_before"
        res_details_before = self.get_res_details(res_file_path_before)
        print("- 2 - CreateResSubcriptions(NFVO->VIM)")
        vimcreatesubscription_timestamp = datetime.now()
        vimcreatesubscription_timeout = 30
        self.req.vim_CreateSubscription()
        print("- 3 - AuthForPushData(VIM->NFVO)")
        nfvo_ip, nfvo_port = utils.get_nfvo_server_ip_port()
        time.sleep(1)
        if debug:
            os.system(
                'curl --cacert /etc/faked_nfvo/server.pem -X POST https://%s:%s/v1/vimTokens -H \'X-Auth-Username:admin\' -H \'X-Auth-Password:admin\' -d \'{"VimId": "123456789012345678901234567890123456"}\'' % (
                    nfvo_ip, nfvo_port))
            print '\n'
        result = utils.wait_response_inlog(vimcreatesubscription_timestamp, vimcreatesubscription_timeout,
                                           resp_kword_map["vimcreatesubscription"], True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        os.system("source ~/openrc "
                  "&& openstack aggregate add host cloudtest node-3.domain.tld")
        # Todo: Wait for PushResPoolInfo request from vim, and validate request schema
        cmd = "nova boot --image ec5b7d9e-0ec4-40b0-b2a4-1aac20f27230 " \
              "--flavor 1 --nic net-id=dad51b0b-c331-4aa8-8201-93b1eac85cd1 " \
              "cloudtest_vim_cm"
        os.system(cmd)
        # Todo: Wait for PushVmChanges request from vim, and validate request schema
        # Todo: Wait for PushCmHeartbeat request from vim, and validate request schema
        res_file_path_after = "./res_file_after"
        res_details_after = self.get_res_details(res_file_path_after)
        self.assertNotEqual(res_details_before, res_details_after,
                            "Not synchronized to the latest vim configuration information")


if __name__ == '__main__':
    unittest.main()
