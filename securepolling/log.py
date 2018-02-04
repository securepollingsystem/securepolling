from sqlite3 import connect
from pickle import loads, dumps

class Log(object):
    def __init__(self, con, table):
        self._con = con
        self._table = table
        cur = self._con.cursor()
        cur.execute('create table if not exists %s(key text primary key, value blob);' % self._table)
        cur.close()

    def scan(self, start, stop):
        '''
        :param bytes start: Start key
        :param bytes stop: Start key
        '''
        cur = self._con.cursor()
        cur.execute('select * from %s where start <= key and key <= stop', self._table)
        for key, value in cur:
            yield key, loads(value)
        cur.close()

    def upsert(self, key, value):
        cur = self._con.cursor()
        cur.execute('insert or replace into %s values (?, ?)' % self._table, key, dumps(value))

    def delete(self, start, stop):
        '''
        Delete by key range.
        :param bytes start: Start key
        :param bytes stop: Start key
        '''
        cur = self._con.cursor()
        cur.execute('delete from %s where start <= key and key <= stop', self._table)
        cur.close()


def partial_log(table):
    def log(path):
        return Log(connect(path), table)
    return log
screed    = partial_log('screed')
tally     = partial_log('tally')
poller    = partial_log('poller')
registrar = partial_log('registrar')
