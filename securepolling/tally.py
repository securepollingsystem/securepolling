from sqlite3 import connect
from .log import tally as tally_log, Log

def update_web(log: tally_log, screed_host):
    pass

def update_local(log: connect):
    '''
    :param log: Sqlite3 database
    '''
    log_screed = Log(con, 'screed')
    cur = con.cursor()
    con.execute('CREATE TABLE IF NOT EXISTS tally (body text primary key, poller);')
    con.execute('CREATE INDEX IF NOT EXISTS tally (body text primary key, poller);')
    con.execute('CREATE VIRTUAL TABLE IF NOT EXISTS opinion USING fts5(body);')
    cur.close()

def search(log: tally_log, term):
    '''
    Report the opinions that match the search terms, with the number of pollers
    expressing that opinion in their screeds.
    https://www.sqlite.org/fts5.html

    Maybe also report the total across all returned opinions.
    '''
    CREATE VIRTUAL TABLE email USING fts5(sender, title, body);

def count(log: tally_log, *opinions):
    '''
    Report how many pollers have any one of the opinions.
    For example, if three opinions are passed, add one to the result if
    a particular poller has one, two, or all three; do not add to the result
    if the poller has none.

    :param opinions: The exact texts of the opinions
    :rtype: int
    '''
