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

    uids = [str(article['uid']) for article in staging_data]
    return uids

def stage_articles():

    stdout = subprocess.call(['sh', './src/sql/stage.sh'])
    if stdout:
        raise Exception('Error: data unsuccessfully staged. Please investigate the logs!')
    teardown_csv('./staging/tmp_article_data.csv')
    return stdout

def push_article(uid):
    
    try:
        with db.PostgreSQL().cursor() as cursor, open('./src/sql/save.sql', 'r') as script:
            sql = script.read()
            cursor.execute(sql, (uid,))
    except Exception as e: 
        """
        Could potentially be more specific here with different errors for different parts of the process, i.e.
        except InitError:  # raised from __init__
            ...
        except AcquireResourceError:  # raised from __enter__
            ...
        except ValueError:  # raised from BLOCK
            ...
        except ReleaseResourceError:  # raised from __exit__
            ...
        """
        raise e
    
    return uid
    
def push_articles():
    
    uids = download_latest_articles()
    staging_status = stage_articles()
    push_status = [push_article(staging_id) for staging_id in uids]
    
    return push_status

if __name__ == '__main__':
    
    push_status = push_articles()
    print(push_status)