#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    import os, sys
    from yoctopuce.yocto_api import *
    from yoctopuce.yocto_anbutton import *
    import subprocess
    import shlex
    import time
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(1)
            
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

scriptname = os.path.basename(sys.argv[0])

print ('LOGITacker injection at the push of two buttons')
print ('This script executes until Ctrl-C is pressed.')
print ('Press and hold Ctrl-C in order to stop this program.')
print (' ')
if sys.argv[2] == "AA:BB:CC:DD:EE":
    print ('Test mode executed. No payload will be executed.')

def main():
    # infinite loop for as many executions as needed
    while 1:
        def usage():
            scriptname = os.path.basename(sys.argv[0])
            print("Usage:")
            #print(scriptname + ' <serial_number>')
            #print(scriptname + ' <logical_name>')
            print(scriptname + ' any <LOGI_HW_ADDR>')
            print('Example: ' + scriptname + ' any AA:BB:CC:DD:EE')
            sys.exit()

        def die(msg):
            sys.exit(msg + ' (check USB cable)')

        errmsg = YRefParam()

        if len(sys.argv) < 3:
            print ('An address for a target dongle must be specified after ' + scriptname + ' any')
            usage()

        argv2_colon_count = 0
        for c in sys.argv[2]:
            if c == ':':
                argv2_colon_count +=1

        if len(sys.argv[2]) != 14 or argv2_colon_count != 4 or not str(sys.argv[2]).isupper():
            print ('The format of the dongle address is incorrect.')
            usage()

        knob_target = sys.argv[1]
        argv2 = sys.argv[2]

        path_to_this_script = os.path.realpath(__file__)
        #print (path_to_this_script)
        parent_folder = os.path.dirname(path_to_this_script)
        #print (parent_folder)
        script_to_execute = (parent_folder + '/logi_target_inject.ksh')
        #print (script_to_execute)
        script_exists_check = os.path.isfile(script_to_execute)
        if not script_exists_check:
            print ('Script to execute not found.')    
        else:
            os.chmod(script_to_execute, 0o700)

        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            sys.exit("init error" + errmsg.value)

        if knob_target == 'any':
            # retrieve any button 
            channel = YAnButton.FirstAnButton()
            if channel is None:
                die('No module connected')
        else:
            channel = YAnButton.FindAnButton(knob_target + '.anButton1')

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
    # two button option is preferred below
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
                #print (button_counter)
            if channel2.get_isPressed() == YAnButton.ISPRESSED_TRUE:
                button_counter +=1
                #print (button_counter)
            if channel3.get_isPressed() == YAnButton.ISPRESSED_TRUE:
                button_counter +=1
                #print (button_counter)
            if channel4.get_isPressed() == YAnButton.ISPRESSED_TRUE:
                button_counter +=1
                #print (button_counter)
            if channel5.get_isPressed() == YAnButton.ISPRESSED_TRUE:
                button_counter +=1
                #print (button_counter)

            #print('(press any two buttons simultaneously to execute)')
            # this is done for safety reasons; might prevent premature execution
            # from an accidental button press
            # two buttons must be pressed for execution
            YAPI.Sleep(100)
            if button_counter >= 2:
                done = True

        YAPI.FreeAPI()
        print('Executing payload...')
        #subprocess.check_call(pass_arg)
        #subprocess.check_call([str(script_to_execute), argv2])
        subprocess.check_call([script_to_execute, argv2])
        #subprocess.Popen(['./logi_target_inject.ksh %s' % argv2])
        #subprocess.call(shlex.split('./logi_target_inject.ksh' + argv2))
        #payload = (str(script_to_execute) + ' ' + str(argv2))
        #subprocess.call(shlex.split(payload))
        #subprocess.Popen(['logi_target_inject.ksh %s' %(argv2)], shell=True)
        #subprocess.Popen(['logi_target_inject.ksh %s' %(argv2)])
        #subprocess.Popen(['%s %s' %(script_to_execute,argv2)])
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
        finally:
            sys.exit(1)

