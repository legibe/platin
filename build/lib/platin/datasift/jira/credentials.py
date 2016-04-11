from os.path import expanduser, join
from ...core.config import Config

class Credentials(object):

    def __init__(self):
        credentials = []

        filename = join(join(expanduser("~"),'.dbs'),'.jira.yaml')
        credentials = Config.read(filename)
        self.username = credentials['username']
        self.password = credentials['password']
