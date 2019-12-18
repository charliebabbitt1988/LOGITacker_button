#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yoctopuce.yocto_api import *
from yoctopuce.yocto_anbutton import *
import subprocess
import shlex

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()

def die(msg):
    sys.exit(msg + ' (check USB cable)')

errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any button 
    channel = YAnButton.FirstAnButton()
    if channel is None:
        die('No module connected')
else:
    channel = YAnButton.FindAnButton(target + '.anButton1')

if not (channel.isOnline()):
    die('device not connected')
else:
    m = channel.get_module()
    channel1 = YAnButton.FindAnButton(m.get_serialNumber() + '.anButton1')
    channel2 = YAnButton.FindAnButton(m.get_serialNumber() + '.anButton2')
    channel3 = YAnButton.FindAnButton(m.get_serialNumber() + '.anButton3')
    channel4 = YAnButton.FindAnButton(m.get_serialNumber() + '.anButton4')
    channel5 = YAnButton.FindAnButton(m.get_serialNumber() + '.anButton5')

# only one button needed for activation
# two button option is uncommented below
#done = False
#while not done:
    #print('(press any button to execute)')
#    done = (channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE) or \
#    (channel2.get_isPressed() == YAnButton.ISPRESSED_TRUE) or \
#    (channel3.get_isPressed() == YAnButton.ISPRESSED_TRUE) or \
#    (channel4.get_isPressed() == YAnButton.ISPRESSED_TRUE) or \
#    (channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE)
#    YAPI.Sleep(100)

done = False
while not done:
    button_counter=0
    if channel1.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        button_counter +=1
        print (button_counter)
    if channel2.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        button_counter +=1
        print (button_counter)
    if channel3.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        button_counter +=1
        print (button_counter)
    if channel4.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        button_counter +=1
        print (button_counter)
    if channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE:
        button_counter +=1
        print (button_counter)

    #print('(press any two buttons to execute)')
    if button_counter >= 2:
        done = True
    YAPI.Sleep(100)

YAPI.FreeAPI()
print('Executing payload...')
#subprocess.call(shlex.split('./logi_target_inject.ksh param1 param2'))
