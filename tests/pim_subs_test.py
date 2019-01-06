#! /usr/bin/python
# coding:utf-8
import unittest
import logging
import test_utils
from faked_nfvo.requests import request_utils
from faked_nfvo.requests.request_vimpim import RequestVIMPIM

conf_util = request_utils.ConfigUtil()
vim_host = conf_util.get("host", "vim")
vim_port = conf_util.get("port", "vim")
scheme = conf_util.get("scheme", "pim")
pim_host = conf_util.get("host", "pim")
pim_port = conf_util.get("port", "pim")


class PimSubScriptionsTest(unittest.TestCase):
    """
        test for case 'PIMops subscription'
    """

    def setUp(self):
        self.request = RequestVIMPIM(vim_host, vim_port, pim_host, pim_port,
                                     scheme)

    def testPimSubs(self):
        nfvoid = conf_util.get("nfvoid", "pim")
        username = conf_util.get("username", "pim")
        password = conf_util.get("password", "pim")
        identity_uri = conf_util.get("identity_uri", "pim")
        subtype = conf_util.get("subtype", "pim")
        period = conf_util.get("period", "pim")
        heart_beat = conf_util.get("heart_beat", "pim")

        # first time to create CreateResSubcriptions
        self.request.pim_CreateSubscription_with_curl(nfvoid, username, password,
                                            identity_uri, subtype, period,
                                            heart_beat)

        self.request.pim_ListSubscriptions_with_curl()

        self.request.pim_DeleteSubscription_with_curl(nfvoid, subtype)

        self.request.pim_ListSubscriptions_with_curl()


if __name__ == '__main__':
    unittest.main()
