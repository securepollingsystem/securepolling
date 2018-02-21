sps='python3 -m securepolling'
rm -f ~/.config/securepolling.json
$sps registrar add_slot /tmp/registrar.sqlite 2018-02-1{7,9}T00:00:00 -length 20
$sps poller create /tmp/registrar.sqlite tom
$sps poller keygen
$sps poller calendar
$sps poller schedule_appointment 2018-02-17T16:34:00
$sps registrar confirm_eligibility /tmp/registrar.sqlite tom
$sps poller confirm_appointment
$sps registrar confirm_eligibility /tmp/registrar.sqlite tom
