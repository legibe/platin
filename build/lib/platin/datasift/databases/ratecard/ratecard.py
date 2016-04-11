# -*- coding: utf-8 -*-
import json
import bisect
from ....core.date import Day
from ....mysql.sqlquery import sqlquery
from ratecardmap import RatecardMap

# utility class using RatecardMap. Once instanciated, you
# call RatecardMap method on this instance, calls are delegated.

class Ratecard(object):

    #------------------------------------------------------------------------
    # db should be a platin.mysql.mysql object pointing to a ratecard
    # database
    #------------------------------------------------------------------------
    def __init__(self,db):
        self._db = db
        self._map = RatecardMap()

    def __getattr__(self,attr):
        return getattr(self._map,attr)

    #------------------------------------------------------------------------
    # returns the detaild for the rate card valid for a particular date
    # if no rate card was found to be valid for that validity date,
    # returns None
    #------------------------------------------------------------------------
    def validRatecard(self,user_id,validity):
        details = None
        # first get all the ratecards sorted by first valid_from, then id
        candidates = self._map.ratecardByUserID(self._db,date=validity,user_id=user_id)

        if candidates:
            # then the valid one is the last one
            elected = candidates[-1]
            # however, the contract has to be valid for our date
            # otherwise we return nothing
            if False and elected['contract_end'] <= validity:
                stop = False
                ref = elected['subscription_number']
                i = len(candidates) - 2
                while not stop:
                    other = candidates[i]
                    if other['subscription_number'] != ref and other['contract_end'] > validity:
                        details = { k:str(i) for k,i in other.items() }
                        stop = True
                    i -= 1
                    if i < 0:
                        stop = True
            else:
                details = { k:str(i) for k,i in elected.items() }

        return details

    #------------------------------------------------------------------------
    # returns the details for a list of rate cards
    # which are valid between 2 dates, first included, last excluded
    #------------------------------------------------------------------------
    def ratecardsInPeriod(self,start,end):
        # by asking for a date in the future we get all ratecards for that user id.
        cards = self._map.ratecardByUserID(self,_db,user_id=user_id,date=Day(30000101))
        valid = []
        unique = set()
        for card in cards:
            if not card['id'] in unique:
                valid.append(Day(card['valid_from']))
                unique.add(card['id'])

    #------------------------------------------------------------------------
    # Returns the JSON content of the ratecard referenced by ID
    #------------------------------------------------------------------------
    def rawRatecardByID(self, id):
        content = self._map.rawRatecardByID(self._db, id=id)
        return json.loads(content)

    #------------------------------------------------------------------------
    # Returns the JSON content of the ratecard referenced by ID
    #------------------------------------------------------------------------
    def ratecardByID(self, id):
        content = self._map.ratecardByID(self._db, id=id)
        return json.loads(content)


    #------------------------------------------------------------------------
    # Returns a list of charges associated with a particular ratecard_id
    #------------------------------------------------------------------------
    def ratecardChargesByID(self, id):
        return self._map.ratecardChargesByID(self._db, id=id)

    #------------------------------------------------------------------------
    # Returns the allowance value of a particular charge in the Ratecard
    #------------------------------------------------------------------------
    def pylonAllowance(self, id, name):
        charges = self.ratecardChargesByID(id)
        try:
            return [int(x['allowance']) for x in charges if x['name'] == name][0]
        except IndexError:
            return None

    #------------------------------------------------------------------------
    # Returns a list of all users with an active ratecard.
    # Can accept user_type 'pylon', 'streaming' or 'all'
    #------------------------------------------------------------------------
    def activeUsers(self, date, user_type='all'):

        # Get all users with a PYLON charge in their ratecard
        if user_type in ['pylon', 'streaming']:
            pylon_users = self._map.ratecardPylonUserIDs(self._db)

        # Get all users with a ratecard
        if user_type in ['streaming', 'all']:
            all_users = self._map.ratecardAllUserIDs(self._db)

        # Select the set of users we are interested in based on user_type
        if user_type == 'pylon':
            users = pylon_users
        elif user_type == 'streaming':
            users = list(set(all_users) - set(pylon_users))
        else: # all
            users = all_users

        # Only return those with a valid ratecard
        return [u for u in users if self.validRatecard(u, date)]
