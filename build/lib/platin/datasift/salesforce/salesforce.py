import re
import os
import datetime
import json
from collections import defaultdict
from platin.core.config import Config

class Salesforce(object):

    id_url = 'https://na1.salesforce.com/%s'

    mapping = {
        'DataSift_UserID__c': 'user_id',
        'User_ID__c': 'user_id',
        'Username_s__c': 'username',
        'Username__c': 'username',
        'Website': 'company_website',
        'Category__c': 'category',
        'SMB_Enterprise__c': 'smb',
        'Contracted_MRR__c': 'price',
        'Subscription_DPU__c': 'allowance',
        'Support_Package__c': 'support',
        'Name': 'company',
       }

    fields = [
              'Id','DataSift_UserID__c','Username_s__c','Name','Owner.Name','OwnerId','Description',
              'Website','Support_Package__c','Customer_Since__c','Contract_Start_Date__c',
              'Contract_End_Date__c','Subscription_Price__c','Subscription_Plan__c',
              'Subscription_DPU__c','Contracted_MRR__c','Category__c','SMB_Enterprise__c',
              'Kirkland_Potential_value_MRR__c','Kirkland_Classification__c'
             ]

    leadFields = [
            'Id','Company','Email','Website','Account_Owner__c','Account_SMB_Enterprise__c',
            'User_ID__c','Username__c'
            ]

    contactFields = [
            'Id','Name','Email', 'User_ID__c','Username__c','Billing_company__c','Description'
            ]

    query = 'SELECT %s FROM %s WHERE %s'

    def __init__(self):
        config = Config.read(os.path.join(os.path.join(os.path.expanduser("~"),'.dbs'),'.sf.yaml'))['credentials']
        self._sf = None
        self._config = config
        self.data = {}
        self.crm = {}

    def sf(self):
        if self._sf is None:
            import simple_salesforce
            self._sf = simple_salesforce.Salesforce(username=self._config['username'], password=self._config['password'], security_token=self._config['token'])
        return self._sf

    # loading, saving
    def load(self,filename=None,leads=True,payg=True,subscription=True):
        if filename is None:
            if leads:
                s = self.paygLeads()
                self.copyStructure(s['records'])
            if payg:
                s = self.paygContacts()
                self.copyStructure(s['records'])
            if subscription:
                s = self.subscriptionAccounts()
                self.copyStructure(s['records'])
                for rec in s['records']:
                    self.crm[rec['Name']] = rec['Id']
        else:
            with open(filename) as f:
                self.data = json.load(f)
                for k in self.data['groups']:
                    self.data['groups'][k] = set(self.data['groups'][k])

    def save(self,filename,pretty=False):
        with open(filename,'w') as f:
            indent = None
            if pretty:
                indent = 4
            json.dump(self.data,f,indent=indent)

    def copyStructure(self,structure):
        self.data['groups'] = defaultdict(set)
        for entry in structure:
            uid = entry.get('DataSift_UserID__c','')
            if uid == '':
                uid = entry.get('User_ID__c','')
            if uid is not None and uid != '':
                tmp = {}
                for k,i in entry.items():
                    if k in self.mapping:
                        k = self.mapping[k]
                    tmp[k] = i
                for k in self.mapping:
                    if not k in tmp:
                        tmp[k] = ''
                try:
                    users = [ int(re.sub('[^0-9]','',x)) for x in uid.split(',') ]
                except ValueError as e:
                    print uid, entry.get('company',''),e
                else:
                    for user in users:
                        self.data[user] = tmp
                        this = entry['Id']
                        if not this in self.data:
                            self.data[this] = []
                        self.data[this].append(user)
                        if 'category' in tmp and tmp['category'] != '':
                            self.data['groups'][tmp['category']].add(user)
                        if 'smb' in tmp and tmp['smb'] != '':
                            self.data['groups'][tmp['smb']].add(user)
        for k in self.data['groups']:
            self.data['groups'][k] = list(self.data['groups'][k])

    # methods on the data structure
    def getLink(self,user_id):
        user_id = str(user_id)
        if user_id in self.data:
            return self.id_url % self.data[user_id]['Id']
        else:
            return ''

    def getUsers(self,sf_id):
        return self.data[sf_id]

    def userGroup(self,group):
        if not group in self.data['groups']:
            return set()
        else:
            return self.data['groups'][group]

    def userGroups(self):
        return self.data['groups'].keys()

    def getField(self,user_id,field):
        user_id = str(user_id)
        if not user_id in self.data:
            return None
        if not field in self.data[user_id]:
            return ''
        return self.data[user_id][field] 

    def getCRM(self):
        return self.crm

    def getSalesRepresentative(self,user_id):
        user_id = str(user_id)
        if not user_id in self.data:
            return None
        return self.data[user_id]['Owner']['Name']

    # method using the salesforce API
    def contractDetailsId(self,user_id):
        where = "Account_Status__c='Customer' and DataSift_UserID__c='%d'" % user_id
        q = self.query % (','.join(self.fields),"Account",where)
        return self.sf().query_all(q)

    def contractDetailsUsername(self,username):
        where = "Account_Status__c='Customer' and Username_s__c='%s'" % username
        q = self.query % (','.join(self.fields),"Account",where)
        return self.sf().query_all(q)

    def subscriptionAccounts(self):
        where = "Account_Status__c='Customer'"
        where = ''
        query = 'SELECT %s FROM %s'
        q = query % (','.join(self.fields),"Account")
        return self.sf().query_all(q)

    def paygLeads(self):
        where = "Total_credit_purchased_ever__c > 10"
        q = self.query % (','.join(self.leadFields),"Lead",where)
        return self.sf().query_all(q)

    def paygContacts(self):
        where = "PAYG_Customer__c = TRUE"
        q = self.query % (','.join(self.contactFields),"Contact",where)
        return self.sf().query_all(q)

