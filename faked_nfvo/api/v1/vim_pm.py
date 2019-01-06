import sys
import logging
from webob import Response

from faked_nfvo.api.schemas import vim_pm
from faked_nfvo.api import wsgi
from faked_nfvo.api import validation


LOG = logging.getLogger(__name__)


class VimPmController(object):

    @validation.schema(request_body_schema=vim_pm.put_pm)
    def put_info(self, req, body):
        LOG.info('Body: %s' % body)
        r = Response()
        r.status = 201

        return r.status
