set -e
sps='python3 -m securepolling'
rm -f ~/.config/securepolling.json /tmp/registrar.sqlite

$sps registrar add_slot /tmp/registrar.sqlite 2018-02-1{7,9}T00:00:00 -length 20
$sps pollee create /tmp/registrar.sqlite tom
$sps pollee calendar
$sps pollee schedule_appointment 2018-02-17T16:34:00
$sps registrar confirm_eligibility /tmp/registrar.sqlite tom yes
$sps pollee confirm_appointment
$sps registrar verify_identity tom
