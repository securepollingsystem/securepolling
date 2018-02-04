from .log import tally as tally_log

def update(log: tally_log, screed_host):
    pass

def search(log: tally_log, term):
    '''
    Report the opinions that match the search terms, with the number of voters
    expressing that opinion in their screeds.

    Maybe also report the total across all returned opinions.
    '''

def count(log: tally_log, *opinions):
    '''
    Report how many voters have any one of the opinions.
    For example, if three opinions are passed, add one to the result if
    a particular voter has one, two, or all three; do not add to the result
    if the voter has none.

    :param opinions: The exact texts of the opinions
    :rtype: int
    '''
