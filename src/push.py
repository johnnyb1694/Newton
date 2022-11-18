import csv
import uuid
import os
import subprocess
import uri
import db

# Utilities

def append_id(list_of_dicts: list):
    
    list_of_dicts = [dict(item, uid=uuid.uuid4()) for item in list_of_dicts]
    return list_of_dicts

def compile_csv(path: str, list_of_dicts: list):

    keys = list_of_dicts[0].keys()
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

def teardown_csv(path: str):
    os.remove(path)
    
# Function Definitions

def download_latest_articles():

    nyt_data = uri.get_latest_nyt()
    guardian_data = uri.get_latest_guardian()
    combined_data = nyt_data + guardian_data

    staging_data = append_id(combined_data)
    compile_csv('./staging/tmp_article_data.csv', staging_data)

def stage_data():

    stdout = subprocess.call(['sh', './src/sql/stage.sh'])
    if stdout:
        raise Exception('Error: data unsuccessfully staged. Please investigate the logs!')
    teardown_csv('./staging/tmp_article_data.csv')
    return stdout

def push_data(uid: str):
    pass
    
if __name__ == '__main__':
    
    download_latest_articles()
    stage_data()