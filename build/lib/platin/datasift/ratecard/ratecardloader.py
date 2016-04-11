import json
import bisect
from ...core.date import Day
from ...mysql.sqlquery import sqlquery

class RatecardLoader(object):

    """
    db should be a platin.mysql.mysql object pointing to a ratecard
    database
    """
    def __init__(self,db):
        self._db = db

    @sqlquery(sql="""
        SELECT id,valid_from,contract_start,contract_end FROM ratecard
        WHERE ':date' >= valid_from AND user_id=:user_id
        ORDER BY valid_from,id
    """)
    def getRatecardByUserID(self,*args,**kwargs):
        pass

    @sqlquery(sql="""
        SELECT content FROM ratecard
        WHERE id=:id
    """)
    def getRatecardByID(self,*args,**kwargs):
        pass

    # call this one if you want details of what was chosen in the database table
    def getRatecardWithDetails(self,user_id,validity):
        details = None
        # first get all the ratecards sorted by first valid_from, then id
        candidates = self.getRatecardByUserID(self._db,date=validity,user_id=user_id)
        result = None
        if len(candidates):
            valid = []
            # convert all datetimes to platin.core.Day
            # gather ordered valid_from in an array
            for c in candidates:
                for key in ('valid_from','contract_start','contract_end'):
                    c[key] = Day(c[key])
                valid.append(c['valid_from'])
            # the bisection tell us where in the sorted array of valid_from where
            # our date would fit (which index). The index will fall right after
            # the index of the rate cards which have the closest lower valid_from
            # if there are valid_from entries in the future of the date, they will
            # be after that index.
            # the correct valid card is the closest (index - 1) unless of course
            # if is 0.
            where = bisect.bisect_right(valid,validity)
            if where > 0:
                where -= 1
            # we know which card we want now
            elected = candidates[where]
            details = elected
            # however, the contract has to be valid for our date
            # otherwise we return nothing
            if elected['contract_end'] <= validity:
                result = None
            else:
                # load the correct rate card and convert the json blob
                rc = self.getRatecardByID(self._db,id=elected['id'])
                result = json.loads(rc[0]['content'])
        return result,details

    # call this one if you just want the data
    def getRatecard(self,user_id,validity):
        rc, details = self.getRatecardWithDetails(user_id,validity)
        return rc
        
