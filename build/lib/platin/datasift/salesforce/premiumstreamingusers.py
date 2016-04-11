import os
from platin.core.config import Config
import simple_salesforce

class PremiumStreaminigUsers(object):

    id_url = 'https://na1.salesforce.com/%s'

    query = """
        SELECT Name, Username_s__c 
        FROM Account 
        WHERE Support_Package__c in ('Premier', 'Elite', 'Elite VIP') and Account_Status__c = 'Customer'
    """

    def __init__(self):
        self._config = Config.read(os.path.join(os.path.join(os.path.expanduser("~"),'.dbs'),'.sf.yaml'))['credentials']

    def users(self):
        usernames = []
        sf = simple_salesforce.Salesforce(username=self._config['username'], password=self._config['password'], security_token=self._config['token'])
        result = sf.query(self.query)
        if len(result):
            for record in result['records']:            
                names = record['Username_s__c']
                collection = [ x.strip() for x in names.split(',') ]
                for c in collection:
                    usernames.append((record['Name'],c))
        usernames.sort()
        return usernames
