#!/usr/bin/env python
# coding=utf-8

from faked_nfvo import wsgi
from faked_nfvo.api.v1 import token
from faked_nfvo.api.v1 import list_subcriptions
from faked_nfvo.api.v1 import vim_cm
from faked_nfvo.api.v1 import vim_fm
from faked_nfvo.api.v1 import pim_fm
from faked_nfvo.api.v1 import vim_pm
from faked_nfvo.api.v1 import pim_pm
from faked_nfvo.api.v1 import pim_cm


vimtoken_controller = token.VIMTokenController()
pimtoken_controller = token.PIMTokenController()
subcription_controller = list_subcriptions.SubcriptionsController()

vim_cm_controller = vim_cm.VimCmController()
vim_pm_controller = vim_pm.VimPmController()
vim_fm_controller = vim_fm.VimFmController()

pim_pm_controller = pim_pm.PimPmController()
pim_fm_controller = pim_fm.PimFmController()
pim_cm_controller = pim_cm.PimCmController()


class RouterApp(wsgi.Router):

    def __init__(self, mapper):

        mapper.connect('/vimTokens',
                       controller=wsgi.Resource(vimtoken_controller),
                       action='get_token',
                       conditions={'method': ['POST']})
        mapper.connect('/pimTokens',
                       controller=wsgi.Resource(pimtoken_controller),
                       action='get_token',
                       conditions={'method': ['POST']})
        mapper.connect('/vimJobs',
                       controller=wsgi.Resource(subcription_controller),
                       action='list',
                       conditions={'method': ['GET']})
        mapper.connect('/vimCm',
                       controller=wsgi.Resource(vim_cm_controller),
                       action='push_info',
                       conditions={'method': ['PUT']})
        mapper.connect('/vimFm',
                       controller=wsgi.Resource(vim_fm_controller),
                       action='get_push_info',
                       conditions={'method': ['PUT']})
        mapper.connect('/pimFm',
                       controller=wsgi.Resource(pim_fm_controller),
                       action='get_push_info',
                       conditions={'method': ['PUT']})
        mapper.connect('/vimPm',
                       controller=wsgi.Resource(vim_pm_controller),
                       action='put_info',
                       conditions={'method': ['PUT']})
        mapper.connect('/pimPm',
                       controller=wsgi.Resource(pim_pm_controller),
                       action='put_info',
                       conditions={'method': ['PUT']})
        mapper.connect('/pimCm',
                       controller=wsgi.Resource(pim_cm_controller),
                       action='push_info',
                       conditions={'method': ['PUT']})

        super(RouterApp, self).__init__(mapper)
