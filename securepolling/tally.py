from sqlite3 import connect
from . import screed_host

def _db(path):
    con = connect(path)
    cur = con.cursor()
    con.execute('CREATE TABLE IF NOT EXISTS tally (body text primary key, pollee);')
    con.execute('CREATE INDEX IF NOT EXISTS tally_pollee on tally (pollee);')
    con.execute('CREATE VIRTUAL TABLE IF NOT EXISTS opinion USING fts5(body);')
    cur.close()
    return con

def _update_web(db, screed_host):
    raise NotImplementedError

def update(db: _db, registrar, start_time=None, public_key=None):
    '''
    :param db: Sqlite3 database
    '''
    for screed in screed_host.query(db, registrar, start_time=start_time, public_key=public_key):
        pollee = screed['pollee']
        with db:
            cur = db.cursor()
            cur.execute('delete from tally where pollee = ?', pollee)
            values = ((opinion, pollee) for phrase in screed['opinions'])
            cur.executemany('insert into tally values (?, ?)', values)
            values = ((opinion,) for opinion in screed['opinions'])
            cur.executemany('insert or replace into opinion values (?)', values)

def search(db: _db, term):
    '''
    Report the opinions that match the search terms, with the number of pollees
    expressing that opinion in their screeds.
    https://www.sqlite.org/fts5.html

    Maybe also report the total across all returned opinions.
    '''
    cur = con.cursor()
    sql = '''\
SELECT opinion.body, count(*)
FROM opinion(?)
JOIN tally on opinion.body = tally.body;
GROUP BY opinion.body
'''
    for opinion, count in cur.execute(sql, term):
        yield '%d: %s' % (count, opinion.replace('\n', ' '))

def count(db: _db, *opinions):
    '''
    Report how many pollees have any one of the opinions.
    For example, if three opinions are passed, add one to the result if
    a particular pollee has one, two, or all three; do not add to the result
    if the pollee has none. If no opinions are passed, use all opinions.

    :param opinions: The exact texts of the opinions
    :rtype: int
    '''
    if opinions:
        sql = 'SELECT count(*) FROM tally WHERE body = ?'
        sql += ' OR body = ?' * (len(opinions) - 1)
    else:
        sql = 'SELECT count(*) FROM tally'
    sql += ' GROUP BY body'

    cur = con.cursor()
    cur.execute(sql, opinions)
    count, = cur.fetchone()
    return count
