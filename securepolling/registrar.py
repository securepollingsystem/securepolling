from sqlite3 import connect
import datetime
from .log import registrar as log_registrar

def Db(x):
    con = connect(x)
    cur = con.cursor()
    cur.execute('create table if not exists slots (start datetime, stop datetime, identity text not null)')
    cur.execute('create table if not exists registrar (identity text primary key, date datetime)')
    cur.close()
    return con

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
            cur.execute("insert into slots (start, stop, identity) values (?, ?, '')",
                        slot_start, slot_stop)
        cur.close()

def confirm_eligibility(identity):
    '''
    Confirm that a particular identity is eligible to poll.
    If the identity has not been submitted before, queue the identity for
    confirmation. If it has been submitted but not reviewed, report the date of
    submission. If it has been reviewed, report the result and, if confirmed,
    subkeys for blinded key submission.

    :param identity: A unique string with information that the registrar will
    use to verify user identity in person.
    '''

def appointment_schedule(identity, blinded_key, appointment_selection):
    '''
    Check that
     
    * the identity's eligibility has been confirmed
    * the selected appointment is available
    * the identity has not selected another upcoming appointment
    
    If all are true, tell the poller and put it on the calendar.
    If any are not, report an error.
    '''

def appointment_availabilities():
    '''
    List available appointment slots.
    '''

def sign_key(identity, date, registrar_key):
    '''
    Record the identity and date, and sign the poller's blinded key (stored
    already in the database) with the registar key.
    '''
