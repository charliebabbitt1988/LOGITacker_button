# LOGITacker_button
beta version 0.1 - 19DEC2019

This is for using a Yocto Knob to inject a payload to a Logitech dongle.
Only Linux is supported.

# install needed packages
- pip3 install yoctopuce
- apt-get install ksh

With an adapter for Micro USB, plug in the Yocto Knob to your Linux computer.  A battery powered Raspberry Pi or Odroid works well.  Also, flash your dongle with the instructions at: https://github.com/mame82/LOGITacker
Plug in your dongle of choice.  The April Brother nRF52840 Dongle is recommended.

If desired, adjust your payload in the logi_target_inject.ksh script near line 25 (default is calc.exe)

## Usage: ./runme.ksh AA:BB:CC:DD:EE  <-- your target

After script is running, approach the target and push two buttons simultaneously on the Yocto Knob.

Usually in close to 5 or 6 seconds, the payload will be sent to the target.  If the payload is larger than one command, then it will take a little longer.

Known issues: 
    - the Yoctopuce libraries for the Yocto Knob are not always 100% reliable so the python script will sometimes fail and not initialize the Yocto Knob; for now the workaround is to execute it in an infinite loop until it executes successfully.  It seems stable after the python script launches.
    - this script uses "pkill screen" in order to bring down the connected screen session to /dev/ttyACM0 which will kill all running screen sessions on the system.  If you need your screen sessions, then don't run this script.
    - the Ctrl-C exit isn't the most graceful, but it works if you hold down the keys.

TODO: 
    - attempt to stabilize the Python script; it doesn't always launch reliably; delays during initializing the Yocto Knob could solve this.
    - optimize the delays between the connections to the screen session so as to make execution faster; total execution time could be as much as 0.25 seconds faster, but not above 0.35 seconds faster; this is working well, however, and probably won't be changed.
    - add support for other platforms like Mac OS X
