from horetu import cli, Program
from . import screed_host, tally, poller, registrar

cli(Program({
    'poller': [
        poller.create,
        poller.tally_hosts,
        poller.keygen,
        poller.screed_add,
        poller.screed_remove,
        poller.screed_list,
        poller.screed_upload,
        poller.tally_pull,
        poller.tally_list,
    ],
    'registrar': [
        registrar.add_slot,
        registrar.list_slots,
        registrar.schedule_appointment,
        registrar.verify_identity,
        registrar.check_eligibility,
        registrar.issue_signature,
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
