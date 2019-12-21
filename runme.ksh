#!/bin/ksh

usage () {
  echo ""
  echo "Usage:"
  echo "${0} <LOGI_HW_ADDR>"
  echo "Example: ${0} AA:BB:CC:DD:EE"
  echo ""
  exit 1
}

if [[ -z $1 ]];then
  echo "No argument passed."
  echo "Target device address is needed."
  echo "Exiting."
  usage
fi

#check the device address input
device_input=$1

#convert to upper case
device_input=$(echo $device_input | tr '[:lower:]' '[:upper:]')

check_length_device=$(echo ${#device_input})
if [[ $check_length_device = "14" ]]; then
  echo ""
else
  echo "The length of the device address is not correct."
  usage
fi

check_colon_count_device=$(echo "${device_input}" | awk -F":" '{print NF-1}')
if [[ $check_colon_count_device = "4" ]]; then
  echo ""
else
  echo "The format of the device address is not correct."
  usage
fi

cwd=$(dirname $0)
cwd=${cwd%/}
clear

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

