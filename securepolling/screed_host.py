from sqlite3 import connect
from pickle import loads, dumps
from sys import stdin

from horetu.annotations import InputFile

from . import util

def _db(path):
    con = connect(path)
    cur = con.cursor()
    cur.execute('''
CREATE TABLE IF NOT EXISTS screed (
  registrar text not null,
  pollee text not null,
  submitted datetime,
  phrases blob,
  primary key (registrar, pollee)
);''')
    cur.close()
    return con

def _registrar_public_key(registrar):
    pass

def _clean_house():
    '''
    Drop all records whose signatures are expired.
    '''

def submit(db: _db, signed_screed):
    '''
    Accept upload of a signed screed with this information.

    * Registrar
    * List of phrases
    * Signature of list of phrases
    * Public key
    * Signature by registrar of public key

    Confirm the signature chain, which involves getting the public key of the
    registrar from the registrar.
    
    If it is valid, upsert it keyed by the registrar and the public key of the
    pollee. Include the current timestamp too.
    '''
    s = util.signed_screed.loads(signed_screed)
    values = (s['registrar'], s['public_key'], dumps(s['phrases']))
    db.execute('insert or replace into screed values (?, ?, ?)', values)

def query(db: _db, registrar, start_time=None):
    '''
    Query for new information.

    :param db: database file
    :param registrar: the registrar's server URL
    :param start_time: get data from this date on (useful for getting only updates)
    '''
    sql = '''\
SELECT pollee, submitted, phrases
FROM screed
WHERE registrar = ?
  AND %d <= submitted
ORDER BY submitted
    ''' % (start_time or '')
    cur = db.cursor()
    for pollee, submitted, phrases in cur.execute(sql, registrar):
        yield {
            'pollee': pollee,
            'submitted': submitted,
            'phrases': loads(phrases),
        }
    cur.close()
