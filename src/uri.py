import os
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

TODAY = datetime.today().date()
LATEST_COMPLETE_DAY = TODAY - timedelta(days = 1)

def parse_datetime(datetime_string: str, pattern: str):
    date = datetime.strptime(datetime_string, pattern).date()
    return date

def request(uri, params, response_format: str = 'json'):
    try:
        response = requests.get(uri, params)
        if response_format == 'json':
            response = response.json()
    except:
        raise Exception('Unable to obtain a response. Check specification of `uri` and `params` arguments.')
    return response

def get_latest_nyt():
    
    uri = 'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json'.format(year = LATEST_COMPLETE_DAY.year, month = LATEST_COMPLETE_DAY.month)
    params = {'api-key': os.environ.get('NYT_API_KEY')}
    
    response = request(uri, params)
    articles = response['response']['docs']
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
            if parse_datetime(a['pub_date'], '%Y-%m-%dT%H:%M:%S+0000') == LATEST_COMPLETE_DAY
            ]
    return data

def get_latest_guardian():

    uri = 'https://content.guardianapis.com/search'
    params = {'show-blocks': 'body', 'from-date': LATEST_COMPLETE_DAY, 'to-date': LATEST_COMPLETE_DAY, 'page-size': 50, 'api-key': os.environ.get('GUARDIAN_API_KEY')}
    
    response = request(uri, params)
    articles = response['response']['results']
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
    pass
