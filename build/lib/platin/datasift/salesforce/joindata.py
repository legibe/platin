import re
from salesforce import Salesforce

class JoinData(object):
    
    def __init__(self):
        self._sf = Salesforce()
        self._sf.load()

    """
        Expects a dictionary with the platform user_id as keys
        each entry is dictionary.
    """
    def join(self,data):
        for user_id,d in data.items():
            d['company'] = self._sf.getField(user_id,'company')
            d['username'] = self._sf.getField(user_id,'username')
            uid = self._sf.getField(user_id,'user_id')
            users = [user_id]
            if uid is not None:
                users = { re.sub('[^0-9]','',x) for x in uid.split(',') }
            d['user_ids'] = users
            d['salesforce'] = self._sf.getLink(user_id)
            d['datasift'] = 'https://datasift.com/admin/user/%d/billing' % int(user_id)
        return data

