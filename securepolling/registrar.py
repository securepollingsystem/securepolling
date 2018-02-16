from logging import getLogger
from sqlite3 import connect
import datetime
from . import util

logger = getLogger(__name__)

def Db(x):
    con = connect(x)
    cur = con.cursor()
    cur.execute('''
create table if not exists slots (
  start datetime, stop datetime,
  identity text not null, blinded_key text not null,
  PRIMARY KEY (start),
  FOREIGN KEY (identity, blinded_key) REFERENCES registrar 
)''')
    cur.execute('''\
CREATE TABLE IF NOT EXISTS registrar (
  identity TEXT NOT NULL,
  blinded_key TEXT NOT NULL,
  submitted DATETIME,
  signed DATETIME,
  subkey TEXT NOT NULL,
  FOREIGN KEY (identity) REFERENCES identities,
  PRIMARY KEY (identity, blinded_key)
)''')
    cur.execute('''\
CREATE TABLE IF NOT EXISTS identities (
  identity TEXT PRIMARY KEY,
  eligible INTEGER,
  confirmed DATETIME
)''')
    cur.close()
    return con
now = datetime.datetime.now

def Natural(x):
    y = int(x)
    if 1 <= y:
        return y
    else:
        raise ValueError('Not a natural number: %d' % y)

def list_slots(db: Db):
    '''
    List appointment slots that are available with the registrar.
    '''
    cur = db.cursor()
    cur.execute('''
SELECT start, stop FROM slots where identity = ''
''')
    yield from cur
    cur.close()

def add_slot(db: Db, start: util.Datetime, stop: util.Datetime, length: Natural=None):
    '''
    Add appointment slots.

    :param start: Start datetime, in %Y-%m-%dT%H:%M:%S format
    :param stop: Stop datetime, in %Y-%m-%dT%H:%M:%S format
    :param length: If set, break the range into slots of this many seconds
        each. If not set, treat the whole range as one time slot.
    '''
    if not start < stop:
        raise ValueError('Start must be before stop.')

    cur = db.cursor()
    cur.execute('''\
SELECT count(*) FROM slots
WHERE ((? < start) AND (start < ?))
   OR ((? < stop ) AND (stop < ?))
   OR ((start < ?) AND (? < stop))
   OR ((start < ?) AND (? < stop));''', (start, stop, start, stop, start, start, stop, stop))
    count, = cur.fetchone()
    if count:
        raise ValueError('New slots overlap with existing slots.')
    cur.close()

    if not length:
        length = stop - start

    with db:
        cur = db.cursor()
        for left in range(int(start.timestamp()), int(stop.timestamp()), length):
            slot_start = datetime.datetime.fromtimestamp(left)
            slot_stop = slot_start + datetime.timedelta(seconds=length - 1)
            cur.execute("insert into slots (start, stop, identity, blinded_key) values (?, ?, '', '')",
                        (slot_start, slot_stop))
        cur.close()

def appointment_availabilities(db: Db):
    '''
    List available appointment slots.
    '''
    cur = db.cursor()
    sql = "select start, stop from slots where ? < start and identity = ''"
    for start, stop in cur.execute(sql, now()):
        yield '%s to %s' % (start, stop)

def schedule_appointment(db: Db, identity, blinded_key, start_time: util.Datetime):
    '''
    Check that

    * the selected appointment is available
    * the identity has not already been verified

    Then queue the identity for eligibility confirmation and
    queue the blinded_key for identity verification.
    '''
    submitted = now()
    cur = db.cursor()
    cur.execute('''\
select count(*) from registrar where signed not null
and identity = ? and blinded_key = ?''', (identity, blinded_key))
    count, = cur.fetchone()
    if count:
        return 'Your identity has already been verified.'
    else:
        cur = db.cursor()
        cur.execute('''\
update slots set identity = ?, blinded_key = ? where start = ? and identity = ''
''', (identity, blinded_key, start_time))
        cur.close()

        cur = db.cursor()
        cur.execute('''\
select count(*) from slots where identity = ? and blinded_key = ? and start = ?
''', (identity, blinded_key, start_time))
        count, = cur.fetchone()
        if count:
            cur.execute('''\
insert into registrar (identity, blinded_key, submitted, subkey)
values (?, ?, ?, '')''', (identity, blinded_key, submitted))
            return '''\
You are tentatively scheduled for %s.
Check again before you go, in case the registrar did not have the chance to
confirm your eligibility beforehand.''' % start_time
        else:
            return 'The appointment at %s is not available.' % start_time

def confirm_eligibility(db: Db, identity):
    '''
    Confirm that a particular identity is eligible to poll.
    '''
    cur = db.cursor()
    cur.execute('update identities set confirmed = 1 where identity = ?',
                now(), identity)

def confirm_ineligibility(db: Db, identity):
    '''
    Confirm that a particular identity is eligible to poll.
    '''
    cur = db.cursor()
    cur.execute('update identities set confirmed = 0 where identity = ?',
                now(), identity)

def check_eligibility(db: Db, identity):
    '''
    Check that the identity's eligibility has been confirmed eligible.
    '''
    logger.critical('TODO: checks')
    cur = db.cursor()
    try:
        confirmed, = next(cur.execute('select confirmed from identities where identity = ?'))
    except StopIteration:
        yield 'Not confirmed'
    else:
        yield 'Confirmed eligible'
        for appointment in cur.execute('...'):
            yield 'Scheduled for %s–%s'

def verify_identity(db: Db, identity):
    '''
    If the identity has not been submitted before, queue the identity for
    confirmation. If it has been submitted but not verified, report the date of
    submission. If it has been reviewed, report the result and, if confirmed,
    subkeys for blinded key submission.

    :param identity: A unique string with information that the registrar will
    use to verify user identity in person.
    '''
    cur = db.cursor()
    rows = list(cur.execute('select * from registrar where identity = ?', identity))
    if rows:
        (identity, submitted, signed, subkey), = rows
        if signed:
            return 'Confirmed on %s\nsubkey: %s' % (signed, subkey)
        else:
            return 'Submitted for review on %s' % submitted
    else:
        cur.execute('insert into registrar values (?, ?, null, \'\')', identity, now())
    cur.commit()
    cur.close()

def issue_signature(db: Db, identity, registrar_key=None):
    '''
    Record the identity and date, and sign the poller's blinded key (stored
    already in the database) with the registar key.
    '''
    raise NotImplementedError
    cur = db.cursor()
    cur = cur.execute('select subkey from registrar where identity = ?', identity)
    try:
        subkey, = next(cur)
    except StopIteration:
        subkey = None
    subkey = util.sign(registrar_key, subkey)

    cur.execute('update registrar set signed = ?, subkey = ? where identity = ?',
                now(), subkey, identity)


    logger.critical('TODO: checks')
