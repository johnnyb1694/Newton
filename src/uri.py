import os
import requests

from dotenv import load_dotenv
load_dotenv()

class URI():

    def __init__(self, root, path, params):
        self.uri = root + path
        self.params = params
    
    def send_request(self):
        response_raw = requests.get(self.uri, params=self.params)
        response_json = response_raw.json()
        return response_json
        
class NYT(URI):

    def __init__(self, year, month):
        path = '{year}/{month}.json'.format(year=year, month=month)
        params = {'api-key': os.environ.get('NYT_API_KEY')}
        URI.__init__(self, root='https://api.nytimes.com/svc/archive/v1/', path=path, params=params)

if __name__ == '__main__':

    nyt = NYT(2020, 9)
    nyt_response = nyt.send_request()
    print(nyt_response)