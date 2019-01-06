# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Simple middleware for request logging."""
import logging

from oslo_utils import excutils
import webob
import webob.dec
import webob.exc
from webob import Response

from faked_nfvo.api import wsgi
from faked_nfvo.token_mgmt import TokenMgmt
from faked_nfvo.api import api_utils

LOG = logging.getLogger(__name__)


class Authenticate(wsgi.Middleware):
    """WSGI Middleware to authenticate the token in request header.

    Borrowed from Paste Translogger
    """
    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        LOG.info("Start authenticating the request from VIM")
        res = Response()
        res.status = "401"
        try:
            res = req.get_response(self.application)
            req_token = req.headers.get('X-Auth-Token')
            if req_token:
                LOG.info("Verify the token in request: %s" % req_token)
                # cached_token_path = os.path.abspath('/tmp/faked_nfvo_api_token')
                cached_token_path = api_utils.get_cached_token_path()
                token_mgmt = TokenMgmt(cached_token_path)
                loc_token = token_mgmt.get_token_id()
                if req_token == loc_token:
                    cached_token = token_mgmt.get_cached_token()
                    LOG.info("Verify the expiry of the token")
                    if not token_mgmt.is_token_expired(cached_token):
                        return res
            else:
                LOG.info("Verify the user name and password in request!")
                req_username = req.headers.get('X-Auth-Username')
                req_password = req.headers.get('X-Auth-Password')
                LOG.info("[username: %s, password: %s]"
                         % (req_username, req_password))
                if req_username == 'admin' and req_password == 'admin':
                    return res
            res.status = "401"
            LOG.error("Authentication failed!")
            return res
        except Exception, e:
            with excutils.save_and_reraise_exception():
                LOG.error("Authentication failed for : %s" % str(e))
        return res
