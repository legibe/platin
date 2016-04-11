import json
from ....core.date import Day
from ....mysql.sqlquery import sqlquery

class RatecardMap(object):

    @sqlquery(sql="""
        SELECT id,valid_from,contract_start,contract_end,subscription_number,cancellation_date
        FROM ratecard
        WHERE ':date' >= valid_from AND user_id=:user_id
        ORDER BY valid_from,id
    """)
    def ratecardByUserID(self,db,date=None,user_id=None,**kwargs):
        pass

    @sqlquery(sql="""
        SELECT content FROM rawcard
        WHERE id=:id
    """)
    def rawRatecardByID(self,db,id=None,result=None,**kwargs):
        return result[0]['content']

    @sqlquery(sql="""
        SELECT content FROM ratecard
        WHERE id=:id
    """)
    def ratecardByID(self,db,id=None,result=None,**kwargs):
        return result[0]['content']

    @sqlquery(sql="""
        SELECT plan_name,rate_type,charge_number,name,charge_model,charge_type,billing_period,price,overage,allowance FROM charge
        WHERE ratecard_id=:id
    """)
    def ratecardChargesByID(self,db,id=None,result=None,**kwargs):
        return result

    @sqlquery(sql="""
        SELECT DISTINCT(user_id) FROM ratecard
    """)
    def ratecardAllUserIDs(self,db,result=None,**kwargs):
        return [i['DISTINCT(user_id)'] for i in result]

    @sqlquery(sql="""
        SELECT DISTINCT(user_id) FROM ratecard
        WHERE id in (SELECT DISTINCT(ratecard_id) FROM charge WHERE plan_name LIKE 'PYLON%')
    """)
    def ratecardPylonUserIDs(self,db,result=None,**kwargs):
        return [i['DISTINCT(user_id)'] for i in result]
