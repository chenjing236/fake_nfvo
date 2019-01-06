__author__ = 'liuying23'


from webob import Response

from faked_nfvo.api.schemas import vim_cm
from faked_nfvo.api import validation


class VimCmController(object):

    @validation.schema(request_body_schema=vim_cm.vim_cm_push_info)
    def push_info(self, req, body):
        r = Response()
        r.status = "201"
        return r
