from platin.core.date import Second
from platin.mysql.authdb import AuthDB
from platin.mysql.sqlquery import sqlquery

class Balances(object):

#    retrieves data from the:
#        - balance, 
#        - balance_report_hourly,
#        - balance_report_daily,
#        - balance_report_monthly
#    tables
    @sqlquery(sql="""
        SELECT user_id,category,unit,source,sum(quantity) AS quantity
        FROM :table 
        WHERE timestamp >= ':start' AND timestamp < ':end'
        GROUP BY user_id,category,unit,source
        ORDER BY user_id,category,unit,source
    """)
    def getSummedUpBalanceData(self,db,table=None,start=None,end=None,**kwargs):
        pass


#   retrieves data from the balance table to check if 
#   which should have been reported in the previous 
#   haven't been reported for some reason
    @sqlquery(sql="""
        SELECT user_id,subscription_number
        FROM balance_period
        WHERE end_period = ':end' and reported=0
    """)
    def getUnreportedData(self,db,end=None,**kwargs):
        pass


