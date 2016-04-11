import json
from collections import defaultdict
from decimal import Decimal
from ...core.date import Date
from ...mysql.authdb import AuthDB

class OldDefinitionManager(object):

    def __init__(self,server='local'):
        self._db = AuthDB(dict(database='definitionmanager',unicode=True,charset='utf8'),server)

    def cleanDates(self,result):
        for field in ['created_at','disabled_at']:
            if field in result:
                result[field] = Date(result[field]).stringvalue()
        return result

    def filterInfo(self,hash,cleanDates=False):
        composite = {}
        result = self._db.select('version',['dpu'],extra_sql="WHERE hash='%s'" % (hash))
        assert(len(result)) < 2
        if len(result) == 0:
            raise IndexError('could not find definition %s' % hash)
        result = result[0]
        for k, i in result.items():
            composite[k] = i
        if cleanDates:
            composite = self.cleanDates(composite)
        return composite
