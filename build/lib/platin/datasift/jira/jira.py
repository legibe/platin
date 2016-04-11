import requests

from credentials import Credentials

class Jira:

    def __init__(self):
        self.credentials = Credentials()
        self.base_url = 'https://jiradatasift.atlassian.net/rest/api/latest/'

    def get_versions(self):
        url = self.base_url + 'project/DPR/versions'
        return requests.get(url, auth=(self.credentials.username, self.credentials.password)).json()

    def get_issues(self, version):
        url = self.base_url + 'search'
        search = 'fixVersion="%s"' %(version)
        return requests.get(url, params={'jql': search}, auth=(self.credentials.username, self.credentials.password)).json()