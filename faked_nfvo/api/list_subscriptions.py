class ListSubcriptions(object):
    def __init__(self, global_conf, local_conf):
        self.global_conf = global_conf
        self.local_conf = local_conf

    def __call__(self, environ, start_response):
        self.__start_verify()
        return ['Version',self.local_conf['version']]

    def __start_verify():
        print 'ListSubcriptions verified'
