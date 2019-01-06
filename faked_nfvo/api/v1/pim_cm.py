from webob import Response

from faked_nfvo.api.schemas import pim_cm
from faked_nfvo.api import validation


class PimCmController(object):

    @validation.schema(request_body_schema=pim_cm.push_cm_info)
    def push_info(self, req, body):
        r = Response()
        r.status = 201

        return r.status