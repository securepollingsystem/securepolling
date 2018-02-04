from .log import screed as screed_log

from horetu.annotations import InputFile

def _registrar_public_key(registrar):
    pass

def _clean_house():
    '''
    Drop all records whose signatures are expired.
    '''

def receive_voter_screed(log: screed_log, signed_screed: InputFile):
    '''
    Accept upload of a signed screed with this information.

    * Registrar
    * List of phrases
    * Signature of list of phrases
    * Public key
    * Signature by registrar of public key

    Confirm the signature chain, which involves getting the public key of the
    registrar from the registrar.
    
    If it is valid, upsert it keyed by the registrar and the public key of the voter.
    Include the current timestamp too.
    '''

def query(log: screed_log, registrar,
          start_time=None, public_key=None):
    '''
    Query for new information.

    :param public_key: Public key prefix
    '''
