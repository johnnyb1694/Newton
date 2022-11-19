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

    uids = [item['uid'] for item in staging_data]
    return uids

def stage_articles():

    stdout = subprocess.call(['sh', './src/sql/stage.sh'])
    if stdout:
        raise Exception('Error: data unsuccessfully staged. Please investigate the logs!')
    teardown_csv('./staging/tmp_article_data.csv')
    return stdout

def push_article(uid: str):
    
    try:
        with db.PostgreSQL().cursor() as cursor, open('./src/sql/save.sql', 'r') as script:
            sql = script.read()
            sql.format(uid = uid)
            cursor.execute(sql)
    except: 
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
        return (uid, -1)
    
    return (uid, 0)
    
def push_articles():
    
    uids = download_latest_articles()
    stage_articles()
    push_status = [push_article(article_id) for article_id in uids]
    
    return push_status

if __name__ == '__main__':
    
    download_latest_articles()
    stage_articles()