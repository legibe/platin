import datetime
import decimal
from ..core.date import Date
from sqldecorator import SQLDecorator

#------------------------------------------------------------------------
# sqlquery is a function or method decorator to write a mySQL select
# request. Example:
#
# from mysql import MySQL
# from sqlquery import sqlquery
#
# class MyQueries(object):
# 
#    @sqlquery("""
#       SELECT sum(quantity), user_id
#       FROM balance
#       WHERE timestamp >= :start 
#             AND timestamp < :end
#             AND unit = ':unit'
#             AND category = ':category'
#       GROUP BY user_id
#    """)
#    def getBalances(self,*args,**kwargs):
#       # you could potentially alter kwargs here before 
#       # they are processed, not recommended for ease of maintenance
#       pass    
#
# query = MyQueries()
# data = query.getBalances(start='2015-08-01',end='2015-09-01,unit='DPU',category='historics')
#------------------------------------------------------------------------

class SQLQuery(SQLDecorator):

    def decorate(self,target,options,this,db,*args,**kwargs):
        # call the target first, just in case it alters
        # some of the arguments (not necessarilly recommended).
        sql = self.SQLStatement(options)
        sql = self.substitute(sql,kwargs)
        result = db.executeSQLAll(sql)
        table,columns = self._get_table_columns(sql)
        if len(columns) == 0:
            columns = db.columns(table)
        values = []
        for value in result:
            d = {}
            for i,c in enumerate(columns):
                d[c] = value[i] 
                if isinstance(value[i],datetime.datetime) or isinstance(value[i],datetime.date):
                    d[c] = Date(value[i])
                elif isinstance(value[i],decimal.Decimal):
                    d[c] = float(value[i])
            values.append(d)
        if this is None:
            result = target(db,result=values,**kwargs)
        else:
            result = target(this,db,result=values,**kwargs)
        if result is None:
            result = values
        return result
sqlquery=SQLQuery
