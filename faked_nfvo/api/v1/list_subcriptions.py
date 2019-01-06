import logging


LOG = logging.getLogger(__name__)


class SubcriptionsController(object):

    def list(self, req):
        LOG.info('ListSubcriptions called')
        return {'subcriptions': 'subcriptions list'}
