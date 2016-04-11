from collections import defaultdict
from platin.core.date import Second
from platin.mysql.authdb import AuthDB
from platin.mysql.sqlquery import sqlquery

class BillingPeriod(object):

#   for a given date, returns a dictionary:
#   subscription_number: {user_id...} as a set
#   for all subscriptions for which the last day
#   in the billing period is date.
    @sqlquery(sql="""
        SELECT user_id, subscription_number
        FROM balance_period
        WHERE end_period = ':date'
    """)
    def endingPeriods(self,db,date=None,result=None,**kwargs):
        r = defaultdict(set)
        for info in result:
            r[info['subscription_number']].add(info['user_id'])
        return r
