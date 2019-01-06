#!/usr/bin/env python

import unittest

from faked_nfvo.requests import pim_request
from faked_nfvo.requests import request_utils
from faked_nfvo.requests.request_vimpim import RequestVIMPIM


class PimCmTest(unittest.TestCase):
    def setUp(self):
        self.req = RequestVIMPIM(request_utils.get_host(),
                                 request_utils.get_port('vim'),
                                 request_utils.get_host(),
                                 request_utils.get_port('pim'))

    def tearDown(self):
        self.req.vim_DeleteSubscription()

    def test_PIMops_cm_scenario(self):
        self.req.vim_CreateSubscription()
        # Todo: Wait for AuthForPushData request from vim, and validate request schema
        # Todo: Wait for PushCmHeartbeat request from vim, and validate request schema
        pim_request.listResDetails()
        # pim_request.listChassisList()
        # pim_request.listChassisDetails()
        # pim_request.listSystemList()
        # pim_request.listSystemDetails()
        # pim_request.listDiskArrayChassisList()
        # pim_request.listDiskArrayChassisDetails()
        # pim_request.listDiskArrayChassisList()
        # pim_request.listDiskArrayChassisDetails()


if __name__ == '__main__':
    unittest.main()