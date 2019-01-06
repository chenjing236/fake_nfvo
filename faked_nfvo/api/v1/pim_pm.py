import sys
import logging
from webob import Response

from faked_nfvo.api.schemas import pim_pm
from faked_nfvo.api import validation


class PimPmController(object):

    @validation.schema(request_body_schema=pim_pm.put_pm)
    def put_info(self, req, body):
        r = Response()
        r.status = 201

        return r.status
