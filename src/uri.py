import os
import requests
import json
import functools

from dotenv import load_dotenv
load_dotenv()

# Utilities 

def check_null_response(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.response is None:
            raise Exception('Please invoke the `request()` method first in order to generate a new response.')
        res = method(self, *args, **kwargs)
        return res
    
    return(wrapper)

# Class Definitions

class URI():
    """
    Creates a 'URI' (i.e. resource) whose response attribute can be updated by calling the 'request()' method.
    """
    def __init__(self, root: str, path: str, params: dict):
        self.root = root
        self.path = path
        self.uri = root + path
        self.params = params
        self.response = None
        self.response_format = 'json'

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
    
    @check_null_response
    def pprint_response(self):
        print(json.dumps(self.response, indent=4, sort_keys=True, ensure_ascii=False))
        
class NYT(URI):

    def __init__(self, year: int, month: int):
        path = '{year}/{month}.json'.format(year=year, month=month)
        params = {'api-key': os.environ.get('NYT_API_KEY')}
        URI.__init__(self, root='https://api.nytimes.com/svc/archive/v1/', path=path, params=params)

    @check_null_response
    def extract_data(self):
        articles = self.response['response']['docs']
        data = [
                {
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

    @check_null_response
    def extract_data(self):
        articles = self.response['response']['results']
        data = [
                {
                'source': 'The Guardian',
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
    
    print(Guardian(from_date='2022-09-01').request().extract_data())
