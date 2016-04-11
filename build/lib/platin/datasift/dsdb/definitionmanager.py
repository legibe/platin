import json
from collections import defaultdict
from decimal import Decimal
from ...core.date import Date
from ...mysql.authdb import AuthDB

class DefinitionManager(object):

    def __init__(self,server='local'):
        self._db = AuthDB(dict(database='definitionmanager',unicode=True,charset='utf8'),server)
        self._tables = ['definition_core','definition_info']
        self._hashes = ['def_definition_id','met_definition_id']
        self._json_columns = set(['csdl_metadata','csdl_summary','meta','source_counts','target_counts'])

    def cleanDates(self,result):
        for field in ['created_at','disabled_at']:
            if field in result:
                result[field] = Date(result[field]).stringvalue()
        return result

    def filterInfo(self,hash,cleanDates=False):
        composite = {}
        for i,table in enumerate(self._tables):
            result = self._db.select(table,extra_sql="WHERE %s='%s'" % (self._hashes[i],hash))
            assert(len(result)) < 2
            if len(result) == 0:
                raise IndexError('could not find definition %s' % hash)
            result = result[0]
            for k, i in result.items():
                if True or k != 'def_definition':
                    k = k[4:]
                    if k in self._json_columns:
                        composite[k] = json.loads(i)
                    elif isinstance(i,Decimal):
                        composite[k] = float(i)
                    else:
                        composite[k] = i
        if cleanDates:
            composite = self.cleanDates(composite)
        return composite

    def dpus(self,hash,price=None):
        result = self.select_all(hash)
        if price is None:
            field = 'dpu_v10'
            if result['tag_version'] == "1.5":
                field = 'dpu_v15'
        else:
            field = price
        return result[field]
