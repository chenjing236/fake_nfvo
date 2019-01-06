import unittest
import json
import os
import logging
from faked_nfvo.requests.request_vimpim import RequestVIMPIM
from faked_nfvo.requests import request_utils
from faked_nfvo.requests import vim_request

LOG = logging.getLogger(__name__)


class VIMPMTest(unittest.TestCase):
    def setUp(self):
        self.req = RequestVIMPIM(request_utils.get_host('vim'),
                                 request_utils.get_port('vim'),
                                 request_utils.get_host('pim'),
                                 request_utils.get_port('pim'))

    def tearDown(self):
        self.req.vim_DeleteSubscription()

    def get_his_metrics(self):
        resp = vim_request.list_history_metrics()
        body = json.loads(resp.body)
        res_file_uri = body.get('FileUri')[0]

        os.system("wget -c %s" % res_file_uri)
        cmd = "tar -xvf %s > filename" % res_file_uri.split('/')[-1]
        os.system(cmd)

        with open("filename") as f:
            filename = f.read()

        with open(filename.split('\n')[0]) as f:
            res_details = f.read()
        res_details_json = json.loads(res_details)
        LOG.info("The metrics file contents:\n %s" % res_details_json)

        return res_details_json

    def test_vim_performance_mgt(self):
        self.req.vim_CreateSubscription()

        # Todo: Wait for AuthForPushData request from vim, and validate request schema
        # Todo: Wait for PushResPoolInfo request from vim, and validate request schema

        per_contents = self.get_his_metrics()

        if not per_contents:
            self.assertIsNone(per_contents, "List history metrics failed")

if __name__ == '__main__':
    unittest.main()


