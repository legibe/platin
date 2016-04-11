from collections import defaultdict
from ...core.date import Date

class DatasiftUsers(object):
    """
    fido and billingpipeline are mysql.mysql.MySQL instance properly connected
    """

    decode = set(['firstname','lastname','company_name','company_website'])

    def __init__(self, fido, billingpipeline):
        sql = """
        SELECT
          user_id,
          plan
        FROM billingpipeline.balance
          LEFT JOIN billingpipeline.user_report
          USING (user_id)
        WHERE plan != 'internal'
              AND ((billingpipeline.user_report.noreport = 0) OR (billingpipeline.user_report.noreport IS NULL));
        """
        users = billingpipeline.executeSQLAll(sql)
        user_info_list = fido.select('user', columns=['id', 'email', 'username',
                                                      'firstname', 'lastname', 'created',
                                                      'company_name', 'company_website'])
        self._plans = defaultdict(set)
        self._users = defaultdict(dict)
        user_info = {}
        for info in user_info_list:
            info['created'] = Date(info['created']).stringvalue()
            user_info[info['id']] = info
            for k,i in info.items():
                if k in self.decode and i is not None:
                    info[k] = i.decode('latin1')
        user_id_indx = 0
        plan_indx = 1
        for user in users:
            uid = user[user_id_indx]
            if uid in user_info:
                info = user_info[uid]
                plan = user[plan_indx]
                if plan == 'custom':
                    plan = 'subscription'
                self._plans[plan].add(uid)
                self._users[uid] = info

    def userInfo(self, user_id):
        return self._users[user_id]

    def users(self):
        return self._users

    def isSubscriptionUser(self, user_id):
        return user_id in self._plans['subscription']

    def subscriptionUsers(self):
        return self._plans['subscription']

    def isPAYGUser(self, user_id):
        return user_id in self._plans['payg']

    def PAYGUsers(self):
        return self._plans['payg']

    def isFreeUser(self, user_id):
        return user_id in self._plans['free']

    def freeUsers(self):
        return self._plans['free']

    @classmethod
    def watchlist(self,fido,billingpipeline):
        sql = """
        SELECT
          user_id,
          plan
        FROM billingpipeline.balance
          LEFT JOIN billingpipeline.user_report
          USING (user_id)
        WHERE plan != 'internal'
              AND (billingpipeline.user_report.noreport = 1);
        """
        users = billingpipeline.executeSQLAll(sql)
        result = {}
        for user in users:
            result[user[0]] = {'plan': user[1] }
        return result
