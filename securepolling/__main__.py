from horetu import cli, Program
from . import screed_host

cli(Program({
    'screed-host': [
        screed_host.receive_voter_screed,
        screed_host.query,
    ],
}, name='securepolling'))
