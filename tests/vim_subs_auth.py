#! /usr/bin/python
# coding:utf-8
import unittest
import logging
import time
from datetime import datetime

import test_utils
import utils
from faked_nfvo.requests import request_utils
from faked_nfvo.requests.request_vimpim import RequestVIMPIM

conf_util = request_utils.ConfigUtil()
vim_host = conf_util.get("host", "vim")
vim_port = conf_util.get("port", "vim")
pim_host = conf_util.get("host", "pim")
pim_port = conf_util.get("port", "pim")

DEBUG = False

resp_kword_map = {
    "vimcreatesubscription": "get_token",
    "pushalarms": "get_push_info",
    "pushcmheartbeat": "vimCm",
    "pushmetrics": "vimFm"
}


class VimSubScriptionsAuthentication(unittest.TestCase):
    """
        test for case 'VIMops subscription and authentication'
    """

    def setUp(self):
        self.request = RequestVIMPIM(vim_host, vim_port, pim_host, pim_port)

    @unittest.skip("skip case:testVimSubsAuth")
    def testVimSubsAuth(self):
        vimcreatesubscription_timeout = 30
        print("- 1 - ListSubscriptions(NFVO->VIM)")
        self.request.vim_ListSubscriptions()

        # first time to create CreateResSubcriptions
        vimcreatesubscription_timestamp = datetime.now()
        nfvo_id = "cloudtest_" + utils.generate_random_string(6)
        print("- 2 - CreateSubscription(NFVO->VIM)")
        self.request.vim_CreateSubscription(nfvo_id)
        print("- 3 - AuthForPushData(VIM->NFVO)")
        if DEBUG:
            test_utils.get_token_from_nfvo(qType="vim")

        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           vimcreatesubscription_timeout,
                                           resp_kword_map["vimcreatesubscription"],
                                           True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request from VIM within 30 seconds.")

        # second time to create CreateResSubcriptions,
        # it will fail because of Repeat subscriptions
        repeat_subs = False
        try:
            print("- 4 - CreateSubscription(NFVO->VIM)")
            self.request.vim_CreateSubscription(nfvo_id)
            # repeat_subs = True
        except:
            pass

        if repeat_subs:
            logging.info(
                "Create subscriptions error:could repeat create subscriptions")
            raise Exception(
                "Create subscriptions error:could repeat create subscriptions")

        time.sleep(10)
        print("- 5 - DeleteSubscription(NFVO->VIM)")
        try:
            self.request.vim_DeleteSubscription(nfvo_id)
        except:
            raise Exception(
                "Failed to delete subscription.")

    # @unittest.skip("skip case:testVimSubsAuth")
    def testVIMSubscriptionUpdate(self):

        # create CreateResSubcriptions
        print("- 1 - CreateSubscription(NFVO->VIM)")
        vimcreatesubscription_timestamp = datetime.now()
        vimcreatesubscription_timeout = 30
        nfvo_id = "cloudtest_" + utils.generate_random_string(6)
        self.request.vim_CreateSubscription(nfvo_id)

        # AuthForPushData(VIM->NFVO)
        print("- 2 - AuthForPushData(VIM->NFVO)")
        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           vimcreatesubscription_timeout,
                                           resp_kword_map["vimcreatesubscription"],
                                           True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request from VIM within 30 seconds.")

        # ListResSubscriptions(NFVO->VIM)
        print("- 3 - ListSubscriptions(NFVO->VIM)")
        self.request.vim_ListSubscriptions()

        # CreateResSubcriptions(NFVO->VIM) update subscription for cm, pm and fm
        print("- 4 - CreateSubscription(NFVO->VIM)")
        vimcreatesubscription_timestamp = datetime.now()
        period = 30
        hb_cm = 60
        hb_fm = 60
        timeout = 10
        self.request.vim_CreateSubscription(nfvo_id, period, hb_cm, hb_fm)

        # ListResSubscriptions(NFVO->VIM)
        print("- 5 - ListSubscriptions(NFVO->VIM)")
        self.request.vim_ListSubscriptions()

        # 6. PushCmHeartbeat(VIM->NFVO)
        print("- 6 - PushCmHeartbeat(VIM->NFVO)")
        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           hb_cm + timeout,
                                           resp_kword_map["pushcmheartbeat"],
                                           True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request from VIM within 30 seconds.")

        # 7. PushMetrics(VIM->NFVO)
        print("- 7 - PushMetrics(VIM->NFVO)")
        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           period + timeout,
                                           resp_kword_map["pushmetrics"],
                                           True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request from VIM within 30 seconds.")
        # 8. PushFmHeartbeat(VIM->NFVO)
        print("- 8 - PushFmHeartbeat(VIM->NFVO)")
        result = utils.wait_response_inlog(vimcreatesubscription_timestamp,
                                           hb_fm + timeout,
                                           resp_kword_map["pushalarms"],
                                           True)
        if result['resp'] and result['validated']:
            print("Got the request and it was validated.")
        else:
            raise Exception(
                "Did not get the request from VIM within 30 seconds.")

        # 9.DeleteResSubcriptions(NFVO->VIM)
        print("- 9 - DeleteSubscription(NFVO->VIM)")
        try:
            self.request.vim_DeleteSubscription(nfvo_id)
        except:
            raise Exception("Failed to delete subscription.")


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(VimSubScriptionsAuthentication("testVimSubsAuth"))
    # suite.addTest(VimSubScriptionsAuthentication("testVIMSubscriptionUpdate"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
