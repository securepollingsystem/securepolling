from horetu import cli, Program
from . import screed_host, tally, poller, registrar

cli(Program({
    'poller': [
        poller.create,
        poller.keygen,
        poller.calendar,
        poller.schedule_appointment, # 1
        poller.confirm_appointment,  # 2
        poller.get_signature,        # 3

        poller.screed_add,
        poller.screed_remove,
        poller.screed_list,
        poller.screed_upload,

        poller.tally_hosts,
        poller.tally_pull,
        poller.tally_list,
    ],
    'registrar': [
        registrar.add_slot,
        registrar.list_slots,
        registrar.verify_identity,
        registrar.check_eligibility,
        registrar.confirm_eligibility,
        registrar.submit_blinded_key,
        registrar.issue_signature,
        registrar.schedule_appointment,
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
