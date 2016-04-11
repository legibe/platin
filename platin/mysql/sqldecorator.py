import re
from platin.core.decorator import Decorator

class SQLDecorator(Decorator):

    def SQLStatement(self,options):
        if not 'sql' in options:
            raise ValueError('the decorator was not given an sql statement as an "sql" argument')
        return options['sql']

    def substitute(self,sql,values):
        result = re.findall('(:\w+)',sql)
        for r in result:
            val = values[r[1:]]
            if isinstance(val,list) or isinstance(val,tuple):
                if isinstance(val[0],basestring):
                    val = ','.join([ "'%s'" % str(x) for x in val ])
                else:
                    val = ','.join([ str(x) for x in val ])
            else:
                val = str(val)
            sql = sql.replace(r,val)
        sql = sql.replace('\n','')
        s = sql.split(' ')
        s = [ x.strip() for x in s if not x == '' ]
        sql = ' '.join(s)
        return sql

    def _get_table_columns(self,sql):
        table = re.findall('FROM (.*?)\s',sql,2)
        if len(table) == 0:
            raise ValueError('cannot find the table')
        table = table[0]
        columns = re.findall('SELECT (.*?) FROM',sql,2)
        if len(columns) == 0:
            raise ValueError('cannot find the columns')
        columns = [ x.strip() for x in columns[0].split(',') ]
        for i, c in enumerate(columns):
            c = c.replace(' AS ',' as ')
            l = c.split(' as ')
            if len(l) > 1:
                columns[i] = l[-1].strip()
        if columns == ['*']:
            columns = []
        return table, columns

