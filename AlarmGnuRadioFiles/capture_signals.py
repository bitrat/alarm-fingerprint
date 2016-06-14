#!/usr/bin/env python

import time
import os
import subprocess
import sys
import itertools

runCapture_433920000_local = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_433920000_local')
runCapture_433920000_external = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_433920000_external')
runCapture_433420000_local = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_434320000_local')
runCapture_433420000_external = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_434320000_external')
runCapture_319500000_local = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_319500000_local')
runCapture_319500000_external = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint', 'AlarmGnuRadioFiles', './run_capture_flowgraph_319500000_external')

def disk_check(diskdir):
   # Before processing any files, check for sufficient space > 40 GB 
    df = subprocess.Popen(["df", diskdir], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
    out = output.split("\n")[1].split()
   # Disk free Space left
    diskspace = int(out[3])

    if diskspace < 40000000:
       print ("\n")
       print ("WARNING: Not enough local disk space.")
       print ("Under 40 GB on local hard drive.")
       print ("Adjust this 40 GB limit, or create some space.")
       print ("\n")
    return diskspace

def option_select(option):
    try :
        select_option = int(raw_input(option))
    except (ValueError, KeyboardInterrupt) as e:
        print ("\n\nInterrupted - Program Exited ...\n")
        quit(0)

    return select_option

def invalid_option_select():
        print ("\n"+"--------------------------------------------------------------------------")
        print ("Invalid option. Try again ....")
        print ("--------------------------------------------------------------------------"+"\n")
        sys.exit()

print (30 * "-")
print ("    ALARM SIGNAL CAPTURE")
print (30 * "-")
print ("1. Local Hard Drive")
print ("2. External Hard Drive")
print (30 * "-")

def freq_select_menu():
    print (44 * "-")
    print ("    SELECT FREQUENCY - TO CAPTURE SIGNALS AT")
    print (44 * "-")
    print ("1. 433.92 MHz (DSC Alexor, Spectra 4000 and Yale Standard)")
    print ("2. 433.42 MHz (Bosch 3000)")
    print ("3. 319.50 MHz (IQPanel)")
    print ("4. Quit")
    print (44 * "-")

while True:
    select_drives = option_select("Select option : ")

    if select_drives == 1:
        # Before running any processing - check diskspace > 40 GB (adjust if needed)
        disk = os.path.join(os.path.sep, os.environ['HOME'], 'alarm-fingerprint','AlarmGnuRadioFiles')
        disk_space = disk_check(disk)
        if disk_space < 40000000:
            print("\n"+"--------------------------------------------------------------------------")
            print ("Not enough local disk space for capturing signals.")
            print("--------------------------------------------------------------------------"+"\n")
            quit(0)
        else:
            freq_select_menu()
            select_freq = option_select("Select option [1-3] : ")
            if  select_freq == 1:
                # Capture at Selected Frequency
                try: 
                    subprocess.call([runCapture_433920000_local], shell=False)
                except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                    print ("\nLocal Capture at 433920000 Hz ... ", e)
                    quit(0)
            elif select_freq == 2:
                # Capture at Selected Frequency
                try: 
                    subprocess.call([runCapture_433420000_local], shell=False)
                except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                    print ("\nLocal Capture at 433420000 Hz ... ", e)
                    quit(0)
            elif select_freq == 3:
                # Capture at Selected Frequency
                try: 
                    subprocess.call([runCapture_319500000_local], shell=False)
                except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                    print ("\nLocal Capture at 319500000 Hz ... ", e)
                    quit(0)
            elif select_freq == 4:
                print("\n"+"--------------------------------------------------------------------------")
                print ("Capture Program stopped.")
                print("--------------------------------------------------------------------------"+"\n")
                quit(0)
            else:
                invalid_option_select()
    elif select_drives == 2:   
        # Before running any processing - check diskspace > 40 GB (adjust if needed)
        if os.path.exists("/media/user/SDRAlarmSignals"):
            disk = os.path.join(os.path.sep, 'media', 'user', 'SDRAlarmSignals')
            disk_space = disk_check(disk)
            if disk_space < 40000000:
                print("\n"+"--------------------------------------------------------------------------")
                print ("Not enough external disk space for capturing signals.")
                print("--------------------------------------------------------------------------"+"\n")
                quit(0)
            else:
                freq_select_menu()
                select_freq = option_select("Select option [1-4] : ")
                if  select_freq == 1:
                    # Capture at Selected Frequency
                    try: 
                        subprocess.call([runCapture_433920000_external], shell=False)
                    except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                        print ("\nExternal drive Capture at 433920000 Hz ... ", e)
                        quit(0)
                elif select_freq == 2:
                    # Capture at Selected Frequency
                    try: 
                        subprocess.call([runCapture_433420000_external], shell=False)
                    except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                        print ("\nExternal drive Capture at 433420000 Hz ... ", e)
                        quit(0)
                elif select_freq == 3:
                    # Capture at Selected Frequency
                    try: 
                        subprocess.call([runCapture_319500000_external], shell=False)
                    except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                        print ("\nExternal drive Capture at 319500000 Hz ... ", e)
                        quit(0)
                elif select_freq == 4:
                    print("\n"+"--------------------------------------------------------------------------")
                    print ("Capture Program stopped.")
                    print("--------------------------------------------------------------------------"+"\n")
                    quit(0)
                else:
                    invalid_option_select()
        else:
            print("\n"+"--------------------------------------------------------------------------")
            print ("External disk drive not connected.")
            print("--------------------------------------------------------------------------"+"\n")
            quit(0)
    else:
        invalid_option_select()

