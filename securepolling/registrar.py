def import_calendar():
    pass

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
    Check that the identity's eligibility has been confirmed and that the
    selected appointment is available. If both are true, tell the poller
    and put it on the calendar. If either is not, report an error.
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
