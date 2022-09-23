import psycopg2
import os

from contextlib import contextmanager

class PostgreSQL():

    def __init__(self, database: str = 'newton', user: str = 'newton', host: str = '127.0.0.1', port: str = '5432'):
        self.database = database
        self._conn = psycopg2.connect(database=database,
                                      user=user,
                                      host=host,
                                      port=port)

    def __repr__(self):
        return f'PostgreSQL connection (to database: {self.database})'
    
    def __str__(self):
        return f'PostgreSQL connection (to database: {self.database})'

    @contextmanager
    def cursor(self, commit: bool = True):
        cursor = self._conn.cursor()
        try:
            yield cursor
        except Exception as e:
            raise Exception('Failed to process transaction. Message: ' + str(e))
        else:
            if commit:
                self._conn.commit()     
        finally:
            cursor.close()
            self._conn.close()

def execute_script(path: str):

    with open(path, 'r').read() as script, PostgreSQL().cursor() as cursor:
        cursor.execute(script)

def init_schema():

    execute_script('./src/sql/schema.sql')

if __name__ == '__main__':

    init_schema()