#!/bin/ksh

usage () {
  echo ""
  echo "Usage:"
  echo "${0} <LOGI_HW_ADDR>"
  echo "Example: ${0} AA:BB:CC:DD:EE"
  echo ""
}

if [[ -z $1 ]];then
  echo "No argument passed."
  echo "Target device address is needed."
  echo "Exiting."
  usage
  exit 1
fi

cwd=$(dirname $0)
cwd=${cwd%/}

# infinite loop needed because the yoctopuce library is not perfect
# the attached Yocto Knob is sometimes not detected
# which causes a catastrophic failure of the python script
# this dirty workaround will launch it again if it fails the first time
while true
do
# ctrl-c terminates
#$cwd/LOGITacker_button.py any $1 || break
$cwd/LOGITacker_button.py any $1
done

