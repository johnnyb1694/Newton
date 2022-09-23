import csv
import uuid

from datetime import datetime
from uri import NYT, Guardian

# Utilities

def append_staging_id(list_of_dicts: list):
    
    list_of_dicts = [dict(item, uid=uuid.uuid4()) for item in list_of_dicts]
    return list_of_dicts

def compile_csv(path: str, list_of_dicts: list):

    keys = list_of_dicts[0].keys()
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

# Function Definitions

def extract_nyt_data():
    """
    Extracts article data from the New York Times 'Archive Search' API for the latest available month.
    """
    year = datetime.now().year
    month = datetime.now().month

    data = NYT(year, month).request().extract_data()
    return data

def extract_guardian_data():
    """
    Extracts article data from the Guardian content API for the newest articles from the latest available month.
    """
    today = datetime.today()
    from_date = datetime(today.year, today.month, 1).date()

    data = Guardian(from_date).request().extract_data()
    return data

def stage_data(path: str = './staging/tmp_article_data.csv'):
    
    nyt_data = extract_nyt_data()
    guardian_data = extract_guardian_data()
    combined_data = nyt_data + guardian_data

    staging_data = append_staging_id(combined_data)
    compile_csv(path, staging_data)

if __name__ == '__main__':
    stage_data()