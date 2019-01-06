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


class PimSubScriptionsAuthTest(unittest.TestCase):
    """
        test for case 'PIMops subscription and authentication'
    """

    def setUp(self):
        self.request = RequestVIMPIM(vim_host, vim_port, pim_host, pim_port,
                                     scheme)

    def testVimSubsAuth(self):
        self.request.pim_ListSubscriptions()

        # first time to create CreateResSubcriptions
        self.request.pim_CreateSubscription()

        # second time to create CreateResSubcriptions,
        # it will fail because of Repeat subscriptions
        repeat_subs = False
        try:
            self.request.pim_CreateSubscription()
            repeat_subs = True
        except:
            pass

        if repeat_subs:
            logging.info(
                "Create subscriptions error:could repeat create subscriptions")
            raise Exception(
                "Create subscriptions error:could repeat create subscriptions")

        test_utils.get_token_from_nfvo(qType="pim")

        self.request.pim_DeleteSubscription()


if __name__ == '__main__':
    unittest.main()
