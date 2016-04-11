from os.path import expanduser, join
from ..core.config import Config
from mysql import MySQL

class AuthDB(MySQL):

    def __init__(self,database,server='local'):
        filename = join(join(expanduser("~"),'.dbs'),'.auth.yaml')
        config = Config.read(filename)
        if not server in config:
            raise IndexError('invalid server name %s' % server)
        config = config[server]
        for k,i in config.items():
            if k != 'mapping':
                database[k] = i
        if server == 'production':
            mapping = config['mapping']
            if database['database'] in mapping:
                database['host'] = mapping[database['database']]
        super(AuthDB,self).__init__(database)
