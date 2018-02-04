from sqlite3 import connect
from .log import tally as tally_log, Log

def _db(path):
    con = connect(path)
    log_screed = Log(con, 'screed')
    cur = con.cursor()
    con.execute('CREATE TABLE IF NOT EXISTS tally (body text primary key, poller);')
    con.execute('CREATE INDEX IF NOT EXISTS tally_poller on tally (poller);')
    con.execute('CREATE VIRTUAL TABLE IF NOT EXISTS opinion USING fts5(body);')
    cur.close()
    return con

def update_web(log: tally_log, screed_host):
    pass

def update_local(db: _db):
    '''
    :param db: Sqlite3 database
    '''

def search(db: _db, term):
    '''
    Report the opinions that match the search terms, with the number of pollers
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
        print('%d: %s' % (count, opinion.replace('\n', ' ')))


def count(db: _db, *opinions):
    '''
    Report how many pollers have any one of the opinions.
    For example, if three opinions are passed, add one to the result if
    a particular poller has one, two, or all three; do not add to the result
    if the poller has none.

    :param opinions: The exact texts of the opinions
    :rtype: int
    '''
    if not opinions:
        raise ValueError('Provide at least one opinion.')

    sql = 'SELECT count(*) FROM tally WHERE body = ?'
    sql += ' OR body = ?' * (len(opinions) - 1)
    sql += ' GROUP BY body'

    cur = con.cursor()
    cur.execute(sql, opinions)
    count, = cur.fetchone()
    return count
