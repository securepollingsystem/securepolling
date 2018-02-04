from horetu import cli, Program
from . import screed_host, tally, poller, registrar

cli(Program({
    'poller': [
        poller.create,
        poller.tally_servers,
        poller.generate_keypair,
        poller.screed_add,
        poller.screed_remove,
        poller.screed_list,
        poller.screed_upload,
    ],
    'registrar-host': [
        registrar.add_slot,
        registrar.confirm_eligibility,
        registrar.sign_key,
        registrar.appointment_schedule,
    ],
    'screed-host': [
        screed_host.submit,
        screed_host.query,
    ],
    'tally': [
        tally.update,
        tally.search,
        tally.count,
    ],
}, name='securepolling'))
