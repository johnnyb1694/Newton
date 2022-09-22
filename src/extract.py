import csv

from datetime import datetime
from uri import NYT, Guardian

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

def compile_csv(path: str, list_of_dicts: list):

    keys = list_of_dicts[0].keys()
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

def stage_data(path: str = './staging/_tmp_article_data.csv'):
    
    nyt_data = extract_nyt_data()
    guardian_data = extract_guardian_data()
    combined_data = nyt_data + guardian_data

    compile_csv(path, combined_data)

if __name__ == '__main__':
    stage_data()