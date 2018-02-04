from horetu import cli, Program
from . import screed_host, tally

cli(Program({
    'screed-host': [
        screed_host.receive_poller_screed,
        screed_host.query,
    ],
    'tally': [
        tally.update,
        tally.search,
        tally.count,
    ],
}, name='securepolling'))
