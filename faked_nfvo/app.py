# All Rights Reserved.
# Copyright Lenovo, Inc
#
# Authors:
#     Yingfu Zhou <zhouyf6@lenovo.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os
import sys
import json
import logging
import logging.config
import socket
import importlib
import webob
import webob.dec
import eventlet
from paste.deploy import loadapp
from OpenSSL import SSL
from eventlet import wsgi
from ConfigParser import SafeConfigParser


def get_external_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@webob.dec.wsgify
def application(req, mod, status):
    res = webob.Response()
    if status:
        res.body = json.dumps(mod.response())
        res.status = 200
    else:
        res.status = 400
    return res


@webob.dec.wsgify.middleware()
def api_verifier(req, app):
    logging.info('--- Request start --- ')
    logging.info(req.method)
    logging.info(req.path_info)
    body = json.loads(req.body)
    logging.info(body)
    logging.info('--- Request end--- ')
    api_name = req.path_info.strip('/').replace('/', '.')
    mod = importlib.import_module('api.%s' % api_name)
    res = mod.verify(body)
    logging.info('Test Result of "%s: %s"' % (api_name, res))
    return app(req, mod, res)


def app_factory(global_config, **local_config):
    return application


def filter_factory(global_config, **local_config):
    return api_verifier


class Resource(object):
    def __init__(self, controller):
        self.controller = controller()

    @webob.dec.wsgify
    def __call__(self, req):
        match = req.environ['wsgiorg.routing_args'][1]
        action = match['action']
        if hasattr(self.controller, action):
            method = getattr(self.controller, action)
            return method(req)
        return webob.exc.HTTPNotFound()


def _configure_logging():
    LOG_FILE_NAME = '/var/log/faked_nfvo.log'

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": LOG_FILE_NAME,
                'mode': 'w+',
                "maxBytes": 1024*1024*5,  # 5 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },

        "root": {
            'handlers': ['default'],
            'level': "DEBUG",
            'propagate': False
        }
    }

    logging.config.dictConfig(LOGGING)


def main():
    _configure_logging()

    ctx = SSL.Context(SSL.SSLv23_METHOD)
    parser = SafeConfigParser()
    parser.read("/etc/faked_nfvo/cfg.ini")
    cert_path = parser.get('DEFAULT', 'CERT')
    server_ip = parser.get('DEFAULT', 'nfvo_server_ip')
    scheme = parser.get('DEFAULT', 'scheme')
    if not server_ip:
        server_ip = get_external_addr()
    server_port = int(parser.get('DEFAULT', 'nfvo_port'))
    ctx.use_privatekey_file(cert_path)
    ctx.use_certificate_file(cert_path)

    LOG = logging.getLogger(__name__)
    config_path = os.path.abspath('/etc/faked_nfvo/api-paste.ini')
    wsgi_app = loadapp('config:%s' % config_path, 'nfvo')
    LOG.info("Starting faked NFVO server at: %s://%s:%d" % (scheme,
                                                            server_ip,
                                                            server_port))
    if 'https' in scheme:
        wsgi.server(eventlet.wrap_ssl(eventlet.listen((server_ip, server_port)),
                                      certfile=cert_path, server_side=True),
                                      wsgi_app)
    elif 'http' in scheme:
        server = eventlet.spawn(wsgi.server,
                                eventlet.listen((server_ip, server_port)),
                                wsgi_app)
        server.wait()
    else:
        LOG.exception('Invalid url scheme specified in config file')
        sys.exit(1)
