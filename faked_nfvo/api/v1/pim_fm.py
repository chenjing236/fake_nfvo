import sys
import logging
from webob import Response

from faked_nfvo.api.schemas import pim_fm
from faked_nfvo.api import validation


class PimFmController(object):

    @validation.schema(request_body_schema=pim_fm.pim_fm_push_info)
    def get_push_info(self, req, body):

        r = Response()
        r.status = 201

        return r.status
