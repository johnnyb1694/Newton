import psycopg2
import click

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

def execute(script: str):

    with PostgreSQL().cursor() as cursor, open(script, 'r') as script:
        sql = script.read()
        cursor.execute(sql)

@click.command()
def init_schema(schema: str = './src/sql/schema.sql'):
    execute(schema)
    click.echo('Database schema successfully initialised.')

if __name__ == '__main__':

    init_schema()