#! /usr/bin/python
# coding:utf-8
__auther__ = "zhangyafeng"

import logging
from ConfigParser import ConfigParser

from faked_nfvo.token_mgmt import TokenMgmt

LOG = logging.getLogger(__name__)


def get_token_backup():
    with open("../../token.txt") as f:
        token = f.read()
        return token


def get_base_url(server_type):
    c = ConfigUtil()
    scheme = c.get("scheme", server_type)
    host = c.get("host", server_type)
    port = c.get("port", server_type)
    base_url = "%s://%s:%s" % (scheme, host, port)
    return base_url


def get_host(server_type):
    c = ConfigUtil()
    return c.get("host", server_type)


def get_port(server_type):
    c = ConfigUtil()
    return c.get("port", server_type)


def get_token():
    c = ConfigUtil()
    print "Request token path: %s" % c.get("cached_token_path", "default")
    token_mgmt = TokenMgmt(c.get("cached_token_path", "default"))
    return token_mgmt.get_token_id()


def get_pim_token(username, password):
    cmd = 'curl -i ' \
          '-H "Content-Type:application/json" ' \
          ' -d  \' '\
          ' {"auth": {' \
          '     "identity": {' \
          '         "methods": ["password"],' \
          '         "password":     {' \
          '             "user": {' \
          '                 "name": "%s", ' \
          '                 "domain": {"id": "default"}, ' \
          '                 "password": "%s" }}}}} \'' \
          ' "http://192.168.50.2:5000/v3/auth/tokens"' % (username, password)
    print cmd
    child = subprocess.call(cmd, shell=True)


def get_header():
    return {"Content-Type": "application/json;charset=UTF-8",
            "X-Auth-Token": get_token()}


class ConfigUtil(object):
    """config utils for vm/pim config"""

    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("/etc/faked_nfvo/vim_pim_config.ini")

    def get(self, key, section):
        return self.parser.get(section, key)
