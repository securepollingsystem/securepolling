from logging import getLogger
from sqlite3 import connect
import datetime

logger = getLogger(__name__)

def Db(x):
    con = connect(x)
    cur = con.cursor()
    cur.execute('create table if not exists slots (start datetime, stop datetime, identity text not null)')
    cur.execute('''\
CREATE TABLE IF NOT EXISTS registrar (
  identity TEXT PRIMARY KEY,
  submitted DATETIME,
  confirmed DATETIME,
  signed DATETIME,
  subkey TEXT NOT NULL
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

class Datetime(object):
    _format = '%Y-%m-%dT%H:%M:%S'
    @staticmethod
    def loads(x):
        return datetime.datetime.strptime(x, Datetime._format)
    @staticmethod
    def dumps(y):
        return datetime.datetime.strftime(x, Datetime._format)

def list_slots(db: Db):
    '''
    List appointment slots that are available with the registrar.
    '''

def add_slot(db: Db, start: Datetime, stop: Datetime, length: Natural=None):
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
WHERE start < slot_start < stop
   OR start < slot_stop < stop
   OR slot_start < start < slot_stop
   OR slot_start < stop < slot_stop;''')
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
            slot_stop = slot_start + (length - 1)
            cur.execute("insert into slots (start, stop, identity) values (?, ?, '', '')",
                        slot_start, slot_stop)
        cur.close()

def verify_identity(db: Db, identity):
    '''
    If the identity has not been submitted before, queue the identity for
    confirmation. If it has been submitted but not reviewed, report the date of
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

def confirm_eligibility(db: Db, identity):
    '''
    Confirm that a particular identity is eligible to poll.
    '''
    cur = db.cursor()
    cur.execute('update registrar set confirmed = ? where identity = ?',
                now(), identity)

def check_eligibility(db: Db, identity, blinded_key, start_time):
    '''
    Check that
     
    * the identity's eligibility has been confirmed
    * the selected appointment is available
    * the identity has not selected another upcoming appointment
    
    If all are true, tell the poller and put it on the calendar.
    If any are not, report an error.

    :param start_time: Start time of the appointment
    '''
    logger.critical('TODO: checks')

    cur = db.cursor()
    sql = "update slots set identity = ? where start = ? and identity = ''"
    cur.execute(sql, identity, start_time)
    sql = "select count(*) from slots set where identity = ? and start = ?"
    count, = next(cur.execute(sql, identity, start_time))
    if count:
        return 'Scheduled'
    else:
        return 'Could not schedule: Slot is already taken'


def appointment_availabilities(db: Db):
    '''
    List available appointment slots.
    '''
    cur = db.cursor()
    sql = "select start, stop from slots where ? < start and identity = ''"
    for start, stop in cur.execute(sql, now()):
        yield '%s to %s' % (start, stop)

def issue_signature(db: Db, identity, date, registrar_key):
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
