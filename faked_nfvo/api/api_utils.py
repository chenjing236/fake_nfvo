from ConfigParser import ConfigParser


def get_cached_token_path():
    c = ConfigUtil()
    return c.get("cached_token_path")


class ConfigUtil(object):
    """config utils for vm/pim config"""

    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("/etc/faked_nfvo/cfg.ini")

    def get(self, key, section="DEFAULT"):
        return self.parser.get(section, key)