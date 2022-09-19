from dotenv import load_dotenv
import requests
import os

load_dotenv()

ENDPOINT_ROOT = 'https://api.nytimes.com/svc/archive/v1/'

def construct_uri(year, month):
    uri = ENDPOINT_ROOT + '{year}/{month}.json'.format(year=year, month=month) + '?api-key=' + os.environ.get('NYT_API_KEY')
    return uri

def get_article_data(year, month):
    uri = construct_uri(year, month)
    raw_response = requests.get(uri)
    response_as_json = raw_response.json()
    return response_as_json

if __name__ == '__main__':
    
    res = get_article_data(2022, 9)
    print(res['response']['docs'][0])