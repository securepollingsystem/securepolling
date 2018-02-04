import datetime
from .log import registrar as log_registrar

def Natural(x):
    y = int(x)
    if 1 <= y:
        return y
    else:
        raise ValueError('Not a natural number: %d' % y)

class Datetime(object):
    _format = '%Y-%m-%dT%H:%M'
    @staticmethod
    def loads(x):
        return datetime.datetime.strptime(x, Datetime._format)
    @staticmethod
    def dumps(y):
        return datetime.datetime.strftime(x, Datetime._format)


def add_slot(log: log_registrar, start: Datetime, stop: Datetime, minutes: Natural=None):
    '''
    Add appointment slots.

    :param start: Start datetime, in %Y-%m-%dT%H:%M format
    :param end: End datetime, in %Y-%m-%dT%H:%M format
    :param minutes: If set, break the range into slots of this many minutes
        each. If not set, treat the whole range as one time slot.
    '''
    if not start < end:
        raise ValueError('Start must be before end.')

    for key, value in log.scan('', Datetime.dumps(stop)):
        slot_start, slot_stop = map(Datetime.loads, key.split('!'))
        if start < slot_start < end or start < slot_end < end or \
                slot_start < start < slot_end or slot_start < end < slot_end:
            raise ValueError('New slots overlap with existing slots.')

    if not length:
        length = stop - start

    for left in range(int(start.timestamp()), int(stop.timestamp()), length*60):
        slot_start = datetime.datetime.fromtimestamp(left)
        slot_end = slot_start + (length - 1) * 60
        key = '%s!%s' % (Datetime.dumps(slot_start), Datetime.dumps(slot_end))
        log.upsert(key, )

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
