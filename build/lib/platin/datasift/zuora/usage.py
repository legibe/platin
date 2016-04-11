import os
import requests
from platin.core.config import Config
from platin.core.date import Day

class Usage(object):

    mapping = {
        'unitOfMeasure': 'unit',
        'accountNumber': 'account_number',
        'subscriptionNumber': 'subscription_number',
        'accountName': 'account_name',
        'chargeNumber': 'charge_number'
    }

    def __init__(self):
        self._config = Config.read(os.path.join(os.path.join(os.path.expanduser("~"),'.dbs'),'.zuora.yaml'))['rest']

    def usageForAccountForPeriod(self,acc_num, start, end):
        headers = {'apiAccessKeyId' : self._config['apiAccessKeyId'],
                   'apiSecretAccessKey': self._config['apiSecretAccessKey'],
                   'content-type': 'application/json'}

        url = '%s/usage/accounts/%s?pageSize=40' % (self._config['urlbase'],acc_num)
        usage= {}
        # be agile and accept strings or objects
        # end is not included so add 1 if equal
        start = Day(start)
        end = Day(end)
        # we use end periods which are not included
        # in the period, se we need to subsctract 
        # one day to compate to the start date reported
        # to zuora.
        if start == end:
            end = start + 1
        start -= 1
        end -= 1
        while url:
            res = requests.get(url, headers=headers)
            for u in res.json()['usage']:
                timestamp = Day(u['startDateTime'])
                if timestamp >= start and timestamp < end:
                    if not u['chargeNumber'] in usage:
                        d = {}
                        for k,i in u.items():
                            key = k
                            if k in self.mapping:
                                key = self.mapping[k]
                            d[key] = i
                            if key == 'unit':
                                d[key] = d[key].lower()
                            usage[u['chargeNumber']] = d
                    else:
                        usage[u['chargeNumber']]['quantity'] += u['quantity']
            try:
                url = res.json()['nextPage']
            except KeyError:
                url = None
        return usage

if __name__ == '__main__':
    usage = Usage()
    print usage.usageForAccountForPeriod('1225','2015-10-01','2015-10-02')
