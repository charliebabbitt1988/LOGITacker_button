#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Revisions - 18-Oct-2023 - optimized script

import os
import sys
import subprocess
import time
from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_anbutton import YAnButton

sys.path.append(os.path.join("..", "..", "Sources"))

scriptname = os.path.basename(sys.argv[0])

def usage():
    print("Usage:")
    print(f"{scriptname} any <LOGI_HW_ADDR>")
    print(f"Example: {scriptname} any AA:BB:CC:DD:EE")
    sys.exit()

def die(msg):
    sys.exit(f"{msg} (check USB cable)")

def main():
    print('LOGITacker injection at the push of two buttons')
    print('This script executes until Ctrl-C is pressed.')
    print('Press and hold Ctrl-C in order to stop this program.')
    print(' ')

    if len(sys.argv) < 3:
        print(f"An address for a target dongle must be specified after {scriptname} any")
        usage()

    if sys.argv[2].count(":") != 4 or len(sys.argv[2]) != 14 or not sys.argv[2].isupper():
        print('The format of the dongle address is incorrect.')
        usage()

    if sys.argv[2] == "AA:BB:CC:DD:EE":
        print('Test mode executed. No payload will be executed.')

    knob_target = sys.argv[1]
    argv2 = sys.argv[2]

    script_to_execute = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logi_target_inject.ksh')

    if not os.path.isfile(script_to_execute):
        print('Script to execute not found.')
        return
    else:
        os.chmod(script_to_execute, 0o700)

    errmsg = YRefParam()
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        die(f"init error {errmsg.value}")

    channel = YAnButton.FirstAnButton() if knob_target == 'any' else YAnButton.FindAnButton(f"{knob_target}.anButton1")
    if channel is None or not channel.isOnline():
        die('No module connected or device not connected')

    m = channel.get_module()
    channels = [YAnButton.FindAnButton(f"{m.get_serialNumber()}.anButton{i}") for i in range(1, 6)]

    while True:
        pressed_buttons = sum(1 for channel in channels if channel.get_isPressed() == YAnButton.ISPRESSED_TRUE)
        if pressed_buttons >= 2:
            break
        YAPI.Sleep(100)

    YAPI.FreeAPI()
    print('Executing payload...')
    subprocess.check_call([script_to_execute, argv2])
    time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(1)
