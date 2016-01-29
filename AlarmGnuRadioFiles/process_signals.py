#!/usr/bin/env python

import time
import os
import subprocess
import sys
import itertools
import logging
import grc_bit_converter
import process_alarm_hex_auto

def check_for_files(endchk, startchk, process, select_process_mode, count_waterfall, alarm_num, alarmType):

    chkFiles = [f for f in os.listdir(capdir)]
    for chkname in chkFiles:
        file_abs = os.path.join(capdir,chkname)

        if os.path.isfile(file_abs):
            if chkname.endswith(endchk) and chkname.startswith(startchk):
                chkname_abs = os.path.join(capdir,chkname)
                if process == "bitconvert":
                    # process into hex - Don Weber's grc_bit_converter.py code
                    grc_bit_converter.set_values(chkname_abs)
                    try:
                        os.remove(chkname_abs)
                    except OSError, e:
                        print "Failed to remove :", chkname_abs
                elif process == "alarmlog":
                    process_alarm_hex_auto.open_hex_file(chkname_abs, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType)

def process_cap_files(fdir, capdir, processdir, flowgraph, origdir, alarmType, select_process_mode, count_waterfall, alarm_num): 

    if os.listdir(capdir) :
        capfiles = [f for f in os.listdir(capdir) if f.endswith('.cap')]
        capfile_abs = []
        for capfile in capfiles:
            capfile_path = os.path.join(capdir,capfile)
            capfile_abs.append(capfile_path)

        # Sort capfiles list, and process oldest .cap file in directory
        capfile_abs.sort(key=lambda x: os.path.getmtime(x))

        if capfile_abs:
            print "Capture file being processed is: ",capfile_abs[0]   
       
            if (select_process_mode == 3):

                if (len(compare_cap_files) > 1):

                    # Compare current capfile_abs[0] to previous .cap file name
                    # If .cap file names are different, set count_waterfall back to 1
                    # If .cap file names are the same, then check if the signal has been processed through all alarm system flowgraphs, before removing .cap file if no signal detected.

                    if (capfile_abs[0] != compare_cap_files[1]):
                        compare_cap_files[0] = 1
                        count_waterfall = compare_cap_files[0]
                        compare_cap_files[1] = capfile_abs[0]

                    else:
                        compare_cap_files[0] += 1
                        count_waterfall = compare_cap_files[0]

                else :
                    # Initialize List
                    compare_cap_files.append(count_waterfall)
                    compare_cap_files.append(capfile_abs[0])

            else:
                count_waterfall = 1  

            # Process .cap file according to the Selected Alarm decimation, symbol rate etc
            try: 
                subprocess.call([runScript, "/", flowgraph, capfile_abs[0], alarmType], shell=False)
            except (subprocess.CalledProcessError,KeyboardInterrupt) as e:
                print "\nrun_addconst_flowgraphs program interrupted ... ", e
                print ("\nrun_addconst_flowgraphs program exited now ...\n")
                quit(0)

    # Remove files not needed
    rmFiles = [f for f in os.listdir(capdir)] 
    for name in rmFiles:
        file_abs = os.path.join(capdir,name)

        if os.path.isfile(file_abs):
            if name.endswith("_AddConst0.dat"):
                try:
                    os.remove(os.path.join(capdir,name))
                except OSError, e:
                    print "Failed to remove : ", os.path.join(capdir,name)
            elif name.startswith("Capture_init.cap"):
                try:
                    os.remove(os.path.join(capdir,name))
                except OSError, e:
                    print "Failed to remove : ", os.path.join(capdir,name)
  
    # Process each lot of captured, then offset, Binary sliced .dat and .dat.txt files
    check_for_files(".dat", "Capture", "bitconvert", select_process_mode, count_waterfall, alarm_num, alarmType)
 
    check_for_files(".txt", "Capture", "alarmlog",select_process_mode, count_waterfall, alarm_num, alarmType)


def disk_check(fdir):
   # Before processing any files, check for sufficient space > 40 GB 
    df = subprocess.Popen(["df", fdir], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
    out = output.split("\n")[1].split()
   # Disk free Space left
    diskspace = int(out[3])

    if diskspace < 40000000:
       print "\n"
       print "WARNING: Not enough local disk space."
       print "Under 40 GB on local hard drive."
       print "Adjust this 40 GB limit, or create some space."
       print "\n"
    return diskspace

def drive_select_menu(driveSET):
    print("\n"+"--------------------------------------------------------------------------")
    print ("Captured Signals processed on "+driveSET+" Hard Drive")
    print("--------------------------------------------------------------------------"+"\n")

def alarm_select_menu():
    print (44 * "-")
    print ("    SELECT ALARM - TO PROCESS CAPTURED FILES")
    print (44 * "-")
    print ("1. Spectra")
    print ("2. DSC Alexxor")
    print ("3. Yale Standard")
    print ("4. Bosch 3000")
    print ("5. Quit")
    print (30 * "-")

def invalid_option_select():
    print("\n"+"--------------------------------------------------------------------------")
    print ("Invalid option. Try again ....")
    print("--------------------------------------------------------------------------"+"\n")
    sys.exit()

def alarm_flowgraph_used(alarmType):
    print("\n"+"--------------------------------------------------------------------------")
    print (alarmType+" flowgraph will be used to process the Captured signal files."+"\n")
    print("--------------------------------------------------------------------------"+"\n")

def logging_setup():
    # Create logger to use across modules
    logger = logging.getLogger('log_alarm_signals')
    try:
        logging.config.fileConfig(fdir+'/conf/logging_console.conf')
    except Exception as error:
        print "Hard Drive unavailable."
        sys.exit()

def option_select(option):
    try :
        select_option = int(raw_input(option))
    except (ValueError, KeyboardInterrupt) as e:
        print ("\n\nInterrupted - Program Exited ...\n")
        quit(0)

    return select_option

def audio_select():
    print (30 * "-")
    print ("    SELECT AUDIO ALERT MODE")
    print (30 * "-")
    print ("1. Audio Alert OFF (No Alert when processing stops)")
    print ("2. Audio Alert ON (Alert when processing stops - TESTING MODE)")
    print ("3. Quit")
    print (30 * "-")

    select_audio_mode = option_select("Select option [1-3] : ")
    if (select_audio_mode == 1) or (select_audio_mode == 2):
        return select_audio_mode
    elif select_audio_mode == 3:
        quit_program()
    else:
        invalid_option_select()

def process_end_text():
    print("\n"+"--------------------------------------------------------------------------")
    print("\n"+"1 Capture file left in directory %s."% capdir)
    print("\n"+"CHECK if your capture device is still Recording !")
    print("\n"+"Press Control+Z to Quit, if no more Captured signals expected.")    
    print("\n"+"--------------------------------------------------------------------------")

def process_mode_select():
    print (30 * "-")
    print ("    SELECT PROCESSING MODE")
    print (30 * "-")
    print ("1. Single Alarm Processing MODE")
    print ("2. CPU Processing MODE")
    print ("3. Waterfall Processing MODE")
    print ("4. Quit")
    print (30 * "-")

def mode_menu(modeType):
    print("\n"+"--------------------------------------------------------------------------")
    print (modeType+" Processing started ....."+"\n")
    print("--------------------------------------------------------------------------"+"\n")

def quit_program():
    print("\n"+"--------------------------------------------------------------------------")
    print ("Quit Program.")
    print("--------------------------------------------------------------------------"+"\n")
    quit(0)

def process(fdir, capdir, processdir, flowgraph, origdir, alarmType, select_process_mode, count_waterfall, select_drives, alarm_num, alarmSETcycle, select_audio_mode):

    # Only process the oldest .cap file in the Captured directory, one at a time
    # Process oldest .cap file, if the number of .cap files in Capture directory is > 1
    while 1:

        capnum = len([f for f in os.listdir(capdir) if f.endswith('.cap')])

        # SINGLE ALARM MODE Processing 
        if (select_process_mode == 1):
            if alarmType == "Spectra4000":
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmType == "YaleStandard":
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmType == "Bosch3000":
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmType == "DSCAlexxor":
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_and_External.py'


        # CPU MODE Processing 
        if (select_process_mode == 2):
            alarmSET = alarmSETcycle.next()
            if alarmSET == "DSCAlexxor":
                alarmType = alarmSET
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_and_External.py'
            elif alarmSET == "Spectra4000":
                alarmType = alarmSET
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'
            elif alarmSET == "YaleStandard":
                alarmType = alarmSET
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_and_External.py'
            elif alarmSET == "Bosch3000":
                alarmType = alarmSET
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_and_External.py'

        # WATERFALL MODE Processing 
        if (select_process_mode == 3):
            alarmSET = alarmSETcycle.next()
            # Move to the next Alarm to process
            # Current order: Spectra 4000 -> Yale Standard -> Bosch 3000 -> DSC Alexor
            if alarmSET == "DSCAlexxor":
                alarmType = "Spectra4000"
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmSET == "Spectra4000":
                alarmType = "YaleStandard"
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmSET == "YaleStandard":
                alarmType = "Bosch3000"
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_and_External.py'

            elif alarmSET == "Bosch3000":
                alarmType = "DSCAlexxor"
                if select_drives == 1:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_only.py'
                elif select_drives == 2:
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_and_External.py'

        if (capnum > 1) :
            # Start processing captured signal .cap files
            print "\n"
            print "Process Signal as Alarm Type: ", alarmType
            if select_process_mode == 1:
                print "Process Mode: SINGLE ALARM MODE"
            elif select_process_mode == 2:
                print "Process Mode: CPU MODE"
            elif select_process_mode == 3:
                print "Process Mode: WATERFALL MODE"
            if select_drives == 1:
                print "Drive used: Local "
            elif select_drives == 2:
                print "Drive used: External"

            print "\n%s capture files remain in directory %s, ready to be processed."% (capnum, capdir)

            # Process files
            process_cap_files(fdir, capdir, processdir, flowgraph, origdir, alarmType, select_process_mode, count_waterfall, alarm_num)

        else :

            if select_audio_mode == 1:
                process_end_text()
                time.sleep(5)
            elif select_audio_mode == 2:
                process_end_text()
                # Audio Alert for Testing purposes, to alert when HackRF has stopped capturing
                text = "Please check the HackRF, is it still capturing signals ?!"
                subprocess.Popen(["espeak", "-s 300", "-v", "en-us", text])
                time.sleep(5)
            elif select_audio_mode == 3:
                quit_program()
            else:
                invalid_option_select()
           

# Used for WATERFALL processing MODE
global count_waterfall
count_waterfall = 1
# For WATERFALL MODE, need to make sure the Capture .cap file is only processed once through each alarm system
compare_cap_files = []

print (30 * "-")
print ("    ALARM SIGNAL PROCESSING")
print (30 * "-")
print ("1. Local Hard Drive")
print ("2. External Hard Drive")
print ("3. Quit")
print (30 * "-")

# Set the Alarms to process (for the quick reconnaissance CPU mode)
# Processing starts with alarmSETcycle[1]
# DSCAlexxor is the last alarm to be processed in Waterfall mode
# Add additional Alarms to the end of this list
alarmSET = ["DSCAlexxor", "Spectra4000", "YaleStandard", "Bosch3000"]
alarm_num = len(alarmSET)
alarmSETcycle = itertools.cycle(alarmSET)

while True:
    select_drives = option_select("Select option [1-3] : ")

    if select_drives == 1:

        # LOCAL SET VARIABLES
        fdir = os.path.join(os.path.sep, os.environ['HOME'], 'AlarmGnuRadioFiles')
        capdir = os.path.join(os.path.sep, os.environ['HOME'], 'AlarmGnuRadioFiles', 'Captured')
        processdir = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/AlarmSignals/Processed'
        origdir = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/AlarmSignals/Original'
        runScript = os.path.join(os.path.sep, os.environ['HOME'], 'AlarmGnuRadioFiles', './run_addconst_flowgraphs')

        # Before running any processing - check diskspace > 40 GB (adjust if needed)
        disk_space = disk_check(fdir)
        if disk_space < 40000000:
            print("\n"+"--------------------------------------------------------------------------")
            print ("Not enough local disk space for capturing signals.")
            print("--------------------------------------------------------------------------"+"\n")
            quit(0)
        else:
            driveSET = "Local"
            drive_select_menu(driveSET)
            process_mode_select()
            select_process_mode = option_select("Select option [1-4] : ") 
            if  select_process_mode == 1:
                modeType = "Single Alarm Mode"
                alarm_select_menu()
                select_alarms = option_select("Select option [1-5] : ")
                if select_alarms == 1:
                    alarmType = "Spectra4000"
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                    alarm_flowgraph_used(alarmType)
                elif select_alarms == 2:
                    alarmType = "DSCAlexxor"
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_only.py'
                    alarm_flowgraph_used(alarmType)
                elif select_alarms == 3:
                    alarmType = "YaleStandard"
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_only.py'
                    alarm_flowgraph_used(alarmType)
                elif select_alarms == 4:
                    alarmType = "Bosch3000"
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_only.py'
                    alarm_flowgraph_used(alarmType)
                elif select_alarms == 5:
                    quit_program()
                else:
                    invalid_option_select()

            elif select_process_mode == 2:
                alarmType = "Spectra4000"
                # Starting Alarm flowgraph
                flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                modeType = "CPU Mode"
                mode_menu(modeType)
            elif select_process_mode == 3:
                alarmType = "Spectra4000"
                # Starting Alarm flowgraph
                flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_only.py'
                modeType = "Waterfall Mode"
                mode_menu(modeType)
            elif select_process_mode == 4:
                quit_program()
            else:
                invalid_option_select()

            # Select Audio Alert ON or OFF
            select_audio_mode = audio_select()

            logging_setup()
            process(fdir, capdir, processdir, flowgraph, origdir, alarmType, select_process_mode, count_waterfall, select_drives, alarm_num, alarmSETcycle, select_audio_mode)

    elif select_drives == 2:
  
            # EXTERNAL HARD DRIVE SET VARIABLES
        fdir = os.path.join(os.path.sep, 'media', 'user', 'SDRAlarmSignals')
        capdir = os.path.join(os.path.sep, 'media', 'user', 'SDRAlarmSignals', 'Captured')
        processdir = '/media/user/SDRAlarmSignals/AlarmSignals/Processed'
        origdir = '/media/user/SDRAlarmSignals/AlarmSignals/Original'
        runScript = os.path.join(os.path.sep, os.environ['HOME'], 'AlarmGnuRadioFiles', './run_addconst_flowgraphs')

        if os.path.exists("/media/user/SDRAlarmSignals"):
            disk_space = disk_check(fdir)
            if disk_space < 40000000:
                print("\n"+"--------------------------------------------------------------------------")
                print ("Not enough external disk space for capturing signals.")
                print("--------------------------------------------------------------------------"+"\n")
                quit(0)
            else:
                driveSET = "External"
                drive_select_menu(driveSET)
                process_mode_select()
                select_process_mode = option_select("Select option [1-4] : ") 
                if select_process_mode == 1:
                    modeType = "Single Alarm Mode"
                    alarm_select_menu()
                    select_alarms = option_select("Select option [1-5] : ")
                    if select_alarms == 1:
                       alarmType = "Spectra4000"
                       flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'
                       alarm_flowgraph_used(alarmType)
                    elif select_alarms == 2:
                        alarmType = "DSCAlexxor"
                        flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/DSC_FileInput_To_BinarySlice_Local_and_External.py'
                        alarm_flowgraph_used(alarmType)
                    elif select_alarms == 3:
                        alarmType = "YaleStandard"
                        flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Yale_FileInput_To_BinarySlice_Local_and_External.py'
                        alarm_flowgraph_used(alarmType)
                    elif select_alarms == 4:
                        alarmType = "Bosch3000"
                        flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Bosch3000_FileInput_To_BinarySlice_Local_and_External.py'
                        alarm_flowgraph_used(alarmType)
                    elif select_alarms == 5:
                        quit_program()
                    else:
                        invalid_option_select()

                elif select_process_mode == 2:
                    alarmType = "Spectra4000"
                    # Starting Alarm flowgraph
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'
                    modeType = "CPU Mode"
                    mode_menu(modeType)
                elif select_process_mode == 3:
                    alarmType = "Spectra4000"
                    # Starting Alarm flowgraph
                    flowgraph = '/home/user/alarm-fingerprint/AlarmGnuRadioFiles/Spectra_FileInput_To_BinarySlice_Local_and_External.py'
                    modeType = "Waterfall Mode"
                    mode_menu(modeType)
                elif select_process_mode == 4:
                    quit_program()
                else:
                    invalid_option_select()

                # Select Audio Alert ON or OFF
                select_audio_mode = audio_select()

                logging_setup()
                process(fdir, capdir, processdir, flowgraph, origdir, alarmType, select_process_mode, count_waterfall, select_drives, alarm_num, alarmSETcycle, select_audio_mode)

        else:
            print("\n"+"--------------------------------------------------------------------------")
            print ("External disk drive not connected.")
            print("--------------------------------------------------------------------------"+"\n")
            quit(0)

    elif select_drives == 3:
        print("\n"+"--------------------------------------------------------------------------")
        print ("Quit Alarm signal processing Program.")
        print("--------------------------------------------------------------------------"+"\n")
        quit(0)

    else:
        invalid_option_select()

