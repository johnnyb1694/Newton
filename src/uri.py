import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

# TODO: 
# -> (Possibly) Abstract 'extract_data()' into base URI class
# -> Figure out how to appropriately extract the textual body from the Guardian API response object

class URI():

    """
    Creates a 'URI' (i.e. resource) whose response attribute can be updated by calling the 'request()' method.
    """

    def __init__(self, root, path, params):
        self.root = root
        self.path = path
        self.uri = root + path
        self.params = params
        self.response = None
        self.response_format = 'json'
    
    def set_uri(self, uri):
        self.uri = uri
        return self
    
    def set_params(self, params):
        if not isinstance(params, dict):
            raise TypeError('Please specify URI parameters as a dictionary object.')
        self.params = params
        return self

    def request(self):
        try:
            response = requests.get(self.uri, params=self.params)
            if self.response_format == 'json':
                response = response.json()
        except:
            raise Exception('Unable to obtain a response. Check specification of `uri` and `params` attributes.')
        else:
            self.response = response
        return self
    
    def pprint_response(self):
        if self.response is None:
            raise Exception('Please invoke the `request()` method first in order to generate a new response.')
        print(json.dumps(self.response, indent=4, sort_keys=True, ensure_ascii=False))
        
class NYT(URI):

    def __init__(self, year, month):
        path = '{year}/{month}.json'.format(year=year, month=month)
        params = {'api-key': os.environ.get('NYT_API_KEY')}
        URI.__init__(self, root='https://api.nytimes.com/svc/archive/v1/', path=path, params=params)

    def extract_data(self):
        if self.response is None:
            raise Exception('Please invoke the `request()` method first in order to generate a new response.')
        articles = self.response['response']['docs']
        data = [
                {
                'id': a['_id'],
                'source': a['source'],
                'publication_date': a['pub_date'],
                'section': a['section_name'],
                'headline': a['headline']['main'],
                'abstract': a['abstract'],
                'body': None
                } 
                for a 
                in articles
                ]
        return data

class Guardian(URI):

    def __init__(self, from_date):
        path = ''
        params = {'show-blocks': 'body', 'from-date': from_date, 'page-size': 50, 'api-key': os.environ.get('GUARDIAN_API_KEY')}
        URI.__init__(self, root='https://content.guardianapis.com/search', path=path, params=params)

    def extract_data(self):
        if self.response is None:
            raise Exception('Please invoke the `request()` method first in order to generate a new response.')
        articles = self.response['response']['results']
        data = [
                {
                'id': a['id'],
                'source': 'Guardian',
                'publication_date': a['webPublicationDate'],
                'section': a['sectionName'],
                'headline': a['webTitle'],
                'abstract': None,
                'body': None
                } 
                for a 
                in articles
                ]
        return data

if __name__ == '__main__':
    pass
