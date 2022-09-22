import csv

from datetime import datetime
from uri import NYT, Guardian

# Shall we have a decorator to stage the outputs of 'generate_*_table()' to a folder-based staging area of our local environment?

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
    from_date = datetime(today.year, today.month, 1)

    data = Guardian(from_date).request().extract_data()
    return data

def stage_data():
    pass

if __name__ == '__main__':
    pass