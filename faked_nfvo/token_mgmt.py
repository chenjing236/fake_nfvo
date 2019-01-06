# Copyright: Lenovo Inc. 2016~2017
# Author: Yingfu Zhou <zhouyf6@lenovo.com>

"""
Base class for ceph management rest clients.
"""

import os
import json
import logging
import datetime
import thread
from ConfigParser import SafeConfigParser

from faked_nfvo.requests import rest_client


ISO8601_FLOAT_SECONDS = '%Y-%m-%dT%H:%M:%S.%fZ'
ISO8601_INT_SECONDS = '%Y-%m-%dT%H:%M:%SZ'
EXPIRY_DATE_FORMATS = (ISO8601_FLOAT_SECONDS, ISO8601_INT_SECONDS)
LOCK = thread.allocate_lock()

LOG = logging.getLogger(__name__)


class TokenMgmt(rest_client.RestClient):
    """
    Base class for all clients.
    """

    def __init__(self, cached_token_path):
        parser = SafeConfigParser()
        parser.read("/etc/faked_nfvo/cfg.ini")
        auth_url = parser.get('DEFAULT', 'keystone_auth_url')
        self.base_url = auth_url
        self.cached_token_path = cached_token_path
        super(TokenMgmt, self).__init__(self.base_url)
        token_expiry_threshold = parser.get('DEFAULT', 'token_expiry_threshold')
        self.token_expiry_threshold = datetime.timedelta(seconds=int(token_expiry_threshold))

    def get_cached_token(self):
        if os.path.exists(self.cached_token_path):
            with open(self.cached_token_path, 'r') as cache_file:
                return json.load(cache_file)
        else:
            LOG.info("No cached token!")
        return ""

    def set_cached_token(self, auth_data):
        with open(self.cached_token_path, 'w') as cache_file:
            LOG.info('Saving auth data to cache...')
            json.dump(auth_data, cache_file)

    def is_token_expired(self, auth_data):
        LOCK.acquire()
        expiry = self._parse_expiry_time(auth_data['access']['token']['expires'])
        LOG.info("%s <= %s" % (expiry, datetime.datetime.utcnow()))
        r = expiry <= datetime.datetime.utcnow()
        if r:
            LOG.info('Token expired, will renew token...')
        LOCK.release()
        return r

    def _parse_expiry_time(self, expiry_string):
        expiry = None
        for date_format in EXPIRY_DATE_FORMATS:
            try:
                expiry = datetime.datetime.strptime(
                    expiry_string, date_format)
                return expiry
            except ValueError:
                pass
        if expiry is None:
            raise ValueError(
                "time data '{data}' does not match any of the"
                "expected formats: {formats}".format(
                    data=expiry_string, formats=self.EXPIRY_DATE_FORMATS))
        return expiry

    def get_token(self):
        cached_token = self.get_cached_token()
        if not cached_token or self.is_token_expired(cached_token):
            os.system("source ~/openrc")
            req = {'auth': {'tenantName': 'admin',
                            'passwordCredentials': {
                                'username': 'admin',
                                'password': 'admin'
                             }
                            }
                  }
            LOG.info("Start authenticating...")
            auth = rest_client.RestClient(self.base_url)
            resp, body = auth.post('/tokens', body=json.dumps(req))
            body = json.loads(body)
            token = body['access']['token']
            self.set_cached_token(body)
            return token
        return cached_token['access']['token']

    def get_token_id(self):
        cached_token = self.get_cached_token()
        if not cached_token or self.is_token_expired(cached_token):
            os.system("source ~/openrc")
            req = {'auth': {'tenantName': 'admin',
                            'passwordCredentials': {
                                'username': 'admin',
                                'password': 'admin'
                            }
                            }
                   }
            LOG.info("Start authenticating...")
            auth = rest_client.RestClient(self.base_url)
            resp, body = auth.post('/tokens', body=json.dumps(req))
            body = json.loads(body)
            token = body['access']['token']['id']
            self.set_cached_token(body)
            return token
        return cached_token['access']['token']['id']

    def get_issued_time(self, token):
        return token['issued_at']

    def get_expires_time(self, issued):
        return self.set_expires_time(issued)

    def set_expires_time(self, issued):
        expiry = datetime.datetime.strptime(issued, ISO8601_FLOAT_SECONDS) \
                 + self.token_expiry_threshold
        expiry_str = expiry.strftime(ISO8601_FLOAT_SECONDS)
        LOG.info("Set expires to %s" % expiry_str)
        cached_token = self.get_cached_token()
        cached_token['access']['token']['expires'] = expiry_str
        self.set_cached_token(cached_token)
        return expiry_str