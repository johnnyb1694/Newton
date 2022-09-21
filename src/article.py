import csv

from datetime import datetime
from uri import NYT, Guardian

def extract_nyt_data():

    year = datetime.now().year
    month = datetime.now().month

    data = NYT(year, month).request().extract_data()

    return data

def extract_guardian_data():

    today = datetime.today()
    from_date = datetime(today.year, today.month, 1)

    data = Guardian(from_date).request().extract_data()

    return data

def generate_metadata_table():
    pass
    
def generate_headline_table():
    pass

def generate_abstract_table():
    pass

def generate_body_table():
    pass

if __name__ == '__main__':
    pass