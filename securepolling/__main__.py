from horetu import cli, Program
from . import screed_host, tally, pollee, registrar

cli(Program({
    'pollee': [
        pollee.create,
        pollee.keygen,
        pollee.calendar,
        pollee.schedule_appointment, # 1
        pollee.confirm_appointment,  # 2
        pollee.get_signature,        # 3

        pollee.screed_add,
        pollee.screed_remove,
        pollee.screed_list,
        pollee.screed_upload,

        pollee.tally_hosts,
        pollee.tally_pull,
        pollee.tally_list,
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
