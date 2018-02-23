from logging import getLogger
from os import makedirs, environ
from pathlib import Path
from json import load, dump as _dump
from functools import partial
from sys import stdout
from statistics import median_high

from horetu import Error
from . import registrar, screed_host, tally, util

dump = partial(_dump, indent=2)

CONFIG = Path(environ['HOME']) / '.config' / 'securepolling.json'
CACHE  = Path(environ['HOME']) / '.cache' / 'securepolling-tally-screed.json'
logger = getLogger(__name__)

def _read(path):
    if path.exists():
        with path.open() as fp:
            data = load(fp)
    else:
        makedirs(path.parent, exist_ok=True)
        data = {}
    return data

def _write(data, path):
    if not path.parent.exists():
        makedirs(path.parent, exist_ok=True)
    with path.open('w') as fp:
        dump(data, fp)

def create(registrar, identity, config=CONFIG, *, force=False):
    '''
    Create an identity.

    Add random salt to identity to prevent others from querying registrars'
    servers on users' behalf, when identity is their real name.

    :param registrar: the registrar's server URL
    :param identity: A unique string with information that the registrar will
    use to verify user identity in person.
    '''
    if config.exists() and not force:
        raise Error('Configuration already exists: %s' % config)

    data = {
        'registrar': registrar,
        'identity': identity,
    }

    if config == '-':
        fp = stdout
    else:
        p = Path(config)
        makedirs(p.parent, exist_ok=True)
        fp = p.open('w')
    dump(data, fp)
    fp.close()
    keygen(config)

def tally_hosts(*tally_hosts, config: Path=CONFIG):
    '''
    Add tally hosts to your configuration.

    :param tally_hosts: tally hosts
    '''
    data = _read(config)
    if 'tally_hosts' not in data:
        data['tally_hosts'] = []
    for tally_host in tally_hosts:
        if tally_host not in data['tally_hosts']:
            data['tally_hosts'].append(tally_host)
    _write(data, config)

def keygen(config: Path=CONFIG):
    '''
    Generates a new keypair and save it.
    If a keypair already exists with a valid registrar signature, return an
    error, otherwise overwrite an existing signature.
    '''
    data = _read(config)

    if {'private_key', 'public_key'}.issubset(data):
        raise Error('You already have a keypair.')
    elif not {'private_key', 'public_key'}.issubset(data):
        data['private_key'], data['public_key'] = util.keygen()
        _write(data, config)

def calendar(config: Path=CONFIG):
    data = _read(config)
    if not 'registrar' in data:
        raise Error('Create an identity first.')
    for start, end in registrar.list_slots(registrar.Db(data['registrar'])):
        yield '%s–%s' % (start, end)

def _signature_valid(registrar, identity):
    '''
    Return true if the locally-stored registrar signature is valid.
    Return false if the registrar signature is expired or not present.
    '''

def _get_signature(registrar, identity):
    '''
    Get the registrar signature for the given identity. This function will
    attempt to retrieve the registrar's signature of user's blinded key, unblind
    it using the stored salt, and return the result (a signature of user's
    public key). If there is no valid signature data supplied by the registrar,
    return None.
    '''
    logger.critical('TODO: Get signature from registrar.')

def schedule_appointment(start_time: util.Datetime, *, config: Path=CONFIG):
    '''
    Schedule to have the registrar verify your eligibility, verify your
    identity, and sign your blinded key.
    '''
    data = _read(config)
    if not {'registrar', 'identity', 'public_key'}.issubset(data):
        raise Error('Create an identity and key first.')
    elif not 'blinding_salt' in data:
        data['blinding_salt'] = 'Fake blinding salt'
        _write(data, config)
    blinded_key = util.blind_key(data['public_key'], data['blinding_salt'])
    return registrar.schedule_appointment(
        registrar.Db(data['registrar']), data['identity'], blinded_key, start_time)

def confirm_appointment(config: Path=CONFIG):
    '''
    Check whether the registrar has confirmed your appointment.
    The registrar needs to verify your eligibility before it.
    '''
    data = _read(config)
    return registrar.check_eligibility(registrar.Db(data['registrar']), data['identity'])

def get_signature(config: Path=CONFIG):
    '''
    Get the signed blinded key from the registrar after you have had
    your identity verified by the registrar.
    '''
    data = _read(config)
    return registrar.issue_signature(data['registrar'], data['identity'])

def screed_add(*messages, config: Path=CONFIG):
    '''
    Add messages to the local screed.
    '''
    data = _read(config)
    if 'screed' not in data:
        data['screed'] = []
    for message in messages:
        if message not in data['screed']:
            data['screed'].append(message)
    _write(data, config)

def screed_remove(*indexes: int, config: Path=CONFIG):
    '''
    Remove messages from the local screed.
    '''
    data = _read(config)
    for i in indexes:
        if 0 <= i < len(data.get('screed', [])):
            del(data['screed'][i])
        else:
            raise Error('Bad screed index: %d' % i)
    _write(data, config)

def screed_list(config: Path=CONFIG):
    '''
    List the current messages in the local screed, along with their indexes.
    '''
    with config.open() as fp:
        data = load(fp)
    for i, message in enumerate(data.get('screed', [])):
        yield '% 5d   %s' % (i, message)

def screed_upload(config: Path=CONFIG):
    '''
    Upload the user's local screed to the registrar. If there is no valid
    signature for the user's registrar, or the server refuses to accept, or
    can't be reached, raise an error.
    '''
    data = _read(config)
    phrases_signature = public_key_signature = 'XXX'
    logger.critical('TODO: Sign stuff.')
    if {'registrar', 'public_key'}.issubset(data):
        blob = util.signed_screed.dumps(
            data['registrar'], data.get('screed', []), phrases_signature,
            data['public_key'], public_key_signature,
        )
        for host in data.get('screed_hosts', []):
            screed_host.submit(screed_host._db(host), blob)
    else:
        raise Error('You need to get your key signed.')

def tally_pull(config: Path=CONFIG, cache: Path=CACHE):
    data = _read(config)
    opinions = _read(cache)

    for host in data.get('tally_hosts', []):
        for opinion, count in tally.count(tally._db(host)):
            if not opinion in opinions:
                opinions[opinion] = {}
            opinions[opinion][host] = count
    _write(opinions, cache)

def tally_list(cache: Path=CACHE):
    opinions = _read(cache)
    for opinion in opinions:
        count = median_high(opinions[opinion].values())
        yield '% 5d   %s' % (count, opinion)
