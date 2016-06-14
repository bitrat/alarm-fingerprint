#!/usr/bin/env python
import os, sys
import re
import string
import shutil
import subprocess
import logging
import logging.config
import datetime
import alarm_fingerprint

auto_logger = logging.getLogger('log_alarm_signals.process_alarm_hex_auto')

def open_hex_file(hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType):

    try:
        with open(hexname) as fp:
            indata = fp.read()
    except IOError:
        print ("\nThe file you are trying to open doesn't exist : \n",hexname)
        print ("\n")
        sys.exit()

    try:
        alarmPreambleSynchDSC, alarmPreambleSynchSpectra, alarmPreambleSynchYale, alarmPreambleSynchBosch, alarmPreambleSynchIQPanel = choose_alarm()
    except Exception as error:
        print ("Hex File could not be processed. Are you defining and returning the alarmPreamble ?")
        sys.exit()    

    alarm_transmit_packets(alarmPreambleSynchDSC, alarmPreambleSynchSpectra, alarmPreambleSynchYale, alarmPreambleSynchBosch, alarmPreambleSynchIQPanel, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType) 

def choose_alarm():

# Hex values within different Alarm signals can be similar
# Make sure the Preamble and Synch word are matched at the beginning of the signal, and are not values in the middle of a signal
# by adding 3 \\x00's at the start for DSC, Spectra and IQPanel (no signal data so far contains 24 zero bits within it)

    alarmPreambleSynchDSC = r"\\x00\\x00\\x00\\x03\\xff\\x55|\\x00\\x00\\x00\\xff\\xd5|\\x00\\x00\\x00\\x0f\\xfd\\x55|\\x00\\x00\\x00\\x3f\\xf5|\\x00\\x00\\x00\\x1f\\xd5|\\x00\\x00\\x00\\x0f\\xd5|\\x00\\x00\\x00\\x01\\xfd\\x55|\\x00\\x00\\x00\\x3f\\x55|\\x00\\x00\\x00\\x7f\\x55|\\x00\\x00\\x00\\x07\\xf5|\\x00\\x00\\x00\\x03\\xf5|\\x00\\x00\\x00\\x0f\\xea|\\x00\\x00\\x00\\xfe\\xaa|\\x00\\x00\\x00\\x01\\xff\\xaa|\\x00\\x00\\x00\\x3f\\xaa|\\x00\\x00\\x00\\x3f\\x55|\\x00\\x00\\x00\\x03\\xfa\\xaa|\\x00\\x00\\x00\\x1f\\xaa|\\x00\\x00\\x00\\x7f\\xea|\\x00\\x00\\x00\\x1f\\xfa\\xaa|\\x00\\x00\\x00\\xfd\\x55|\\x00\\x00\\x00\\x07\\xfe\\xaa|\\x00\\x00\\x00\\x07\\xea|\\x00\\x00\\x00\\x01\\xfa\\xaa|\\x00\\x00\\x00\\x7e\\xaa"

    alarmPreambleSynchSpectra = r"\\x00\\x00\\x00\\x01\\xff\\xff\\xff\\xfe|\\x00\\x00\\x00\\x03\\xff\\xff\\xff\\xfc|\\x00\\x00\\x00\\x07\\xff\\xff\\xff\\xf8|\\x00\\x00\\x00\\x0f\\xff\\xff\\xff\\xf0|\\x00\\x00\\x00\\x1f\\xff\\xff\\xff\\xe0|\\x00\\x00\\x00\\x3f\\xff\\xff\\xff\\xc0|\\x00\\x00\\x00\\x7f\\xff\\xff\\xff\\x80|\\x00\\x00\\x00\\xff\\xff\\xff\\xff\\x01|\\x00\\x00\\x00\\x01\\xff\\xff\\xff\\xff|\\x00\\x00\\x00\\x03\\xff\\xff\\xff\\xfe|\\x00\\x00\\x00\\x07\\xff\\xff\\xff\\xfc|\\x00\\x00\\x00\\x0f\\xff\\xff\\xff\\xf8|\\x00\\x00\\x00\\x1f\\xff\\xff\\xff\\xf0|\\x00\\x00\\x00\\x3f\\xff\\xff\\xff\\xe0|\\x00\\x00\\x00\\x7f\\xff\\xff\\xff\\xc0|\\x00\\x00\\x00\\xff\\xff\\xff\\xff\\x80|\\x00\\x00\\x00\\x01\\xff\\xff\\xff\\xff\\x80|\\x00\\x00\\x00\\x03\\xff\\xff\\xff\\xff\\x01|\\x00\\x00\\x00\\x07\\xff\\xff\\xff\\xfe|\\x00\\x00\\x00\\x0f\\xff\\xff\\xff\\xfc|\\x00\\x00\\x00\\x1f\\xff\\xff\\xff\\xf8|\\x00\\x00\\x00\\x3f\\xff\\xff\\xff\\xf0|\\x00\\x00\\x00\\x7f\\xff\\xff\\xff\\xe0|\\x00\\x00\\x00\\xff\\xff\\xff\\xff\\xc0|\\x00\\x00\\x00\\x01\\xff\\xff\\xff\\xff\\xc0|\\x00\\x00\\x00\\x03\\xff\\xff\\xff\\xff\\x80|\\x00\\x00\\x00\\x07\\xff\\xff\\xff\\xff|\\x00\\x00\\x00\\x0f\\xff\\xff\\xff\\xfe|\\x00\\x00\\x00\\x1f\\xff\\xff\\xff\\xfc|\\x00\\x00\\x00\\x03\\xff\\xff\\xff\\xf8|\\x00\\x00\\x00\\x7f\\xff\\xff\\xff\\xf0|\\x00\\x00\\x00\\xff\\xff\\xff\\xff\\xe0"

    alarmPreambleSynchYale = r"\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x01\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x03\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x07\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x0f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x1f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x3f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff"

    alarmPreambleSynchBosch = r"\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x01\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x03\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x07\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x1f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x3f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff|\\x7f\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff"

    alarmPreambleSynchIQPanel = r"\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x03\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x07\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x0f\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x3f\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x7f\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\xff|\\x00\\x00\\x00\\x00\\x00\\x00\\x1f\\xff"

    return alarmPreambleSynchDSC, alarmPreambleSynchSpectra, alarmPreambleSynchYale, alarmPreambleSynchBosch, alarmPreambleSynchIQPanel

def keep_or_remove_alarm_capture_file(pattern, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType):

#Find positions in Alarm hex string to extract packets from
    patternPositions = re.finditer(pattern,indata)
    count = 0
    countSig = 0
    output_to_log = []
    for match in patternPositions:
   
# Packet Data = Status of Device and Serial number
        matchPreamble = match.group(0)       
        extractPacketStart = match.start()
        signal, output = alarm_fingerprint.extract_packet(matchPreamble, extractPacketStart, alarmType, indata, count)
        if signal>0:
           countSig = countSig+1
           # append the output into a list that will be logged
           output_to_log.append(output)
           
    # if countSig greater than 0, then keep original signals, and move them on the last countSig loop
    if countSig>0:
        # Write identified alarm signal results out to a log file
        logflag = "alarmlogfile"
        log_header(hexname, alarmType, pattern, fdir, logflag)

        # Could use a generator function here instead of the 2 for loops
        for index, output_item in enumerate(output_to_log): 
            for list_index, list_output_item in enumerate(output_item):
                if output_item[list_index] != "":
                    auto_logger.info(list_output_item)

        # Move into AlarmSignals/Processed directory          
        move_alarm_signals(capdir, processdir, hexname, fdir)
        # Move .cap file after all processing is completed - containing Alarm Signals
        # Move into AlarmSignals/Original directory
        move_alarm_signals(capdir, origdir, hexname, fdir)

    else:
        auto_logger.debug("--------------------------------")
        auto_logger.debug("--------------------------------")
        auto_logger.debug("Remove files. No properly identifiable "+alarmType+" Signals.")
        #Remove Capture.dat.txt files
        delete_nonalarm_files(capdir, hexname, select_process_mode, count_waterfall, alarm_num, alarmType) 


def log_header(hexname, alarmType, patternMatch, fdir, logflag):
    processfile = hexname.rsplit("/", 1)
    if logflag == "alarmlogfile":
        log_capfile = processfile[1].rsplit(".cap", 1)
        log_addconst = log_capfile[1].rsplit("_", 1)
        # Start log file only if a proper Alarm signal is found after full processing (not just on preamble/synchword match)
        logname = 'logged_alarm_signals_'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+"_"+log_capfile[0]+log_addconst[0]

        logging.config.fileConfig(fdir+'/conf/logging_file.conf', defaults={'logfilename': logname},disable_existing_loggers=False)
        auto_logger.info("--------------------------------")
        auto_logger.info("////////////////////////////////")
        auto_logger.info("--------------------------------")
        auto_logger.info(processfile[1])
        auto_logger.info("--------------------------------\n")
    else :
        # Log to console
        logging.config.fileConfig(fdir+'/conf/logging_console.conf',disable_existing_loggers=False)
        auto_logger.debug("%s Alarm Pattern(s) Matched:\n%s\n", alarmType, patternMatch)
        auto_logger.info("--------------------------------")
        auto_logger.info("////////////////////////////////")
        auto_logger.info("--------------------------------")
        auto_logger.info(processfile[1])
        auto_logger.info("--------------------------------")

def match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag):
    if patternMatch:

        log_header(hexname, alarmType, patternMatch, fdir, logflag)
        # Decision to keep or remove Alarm Signal capture file, based on signal content
        keep_or_remove_alarm_capture_file(pattern, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType)

    else:
    # If ALL signal offset files have no alarm signals in them
        auto_logger.debug("--------------------------------")
        auto_logger.debug("--------------------------------")
        auto_logger.debug("Remove files.  No "+alarmType+" signals at all.")
        delete_nonalarm_files(capdir, hexname, select_process_mode, count_waterfall, alarm_num, alarmType)


def alarm_transmit_packets(alarmPreambleSynchDSC, alarmPreambleSynchSpectra, alarmPreambleSynchYale, alarmPreambleSynchBosch, alarmPreambleSynchIQPanel, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType):

    logflag = "cmdline" 
    # Process any matched Preambles - extract Full Packets
    if alarmType == "Spectra4000":

    # Match Spectra 4000
        pattern = re.compile(alarmPreambleSynchSpectra)
        patternMatch = re.findall(pattern,indata) 
        match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag)

    elif alarmType == "DSCAlexxor":
    # Match DSC Alexxor
        pattern = re.compile(alarmPreambleSynchDSC)
        patternMatch = re.findall(pattern,indata)
        match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag)

    elif alarmType == "YaleStandard":
    # Match Yale
        pattern = re.compile(alarmPreambleSynchYale)
        patternMatch = re.findall(pattern,indata)  
        match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag)

    elif alarmType == "Bosch3000":
    # Match Bosch
        pattern = re.compile(alarmPreambleSynchBosch)
        patternMatch = re.findall(pattern,indata)  
        match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag)

    elif alarmType == "IQPanel":
    # Match IQPanel
        pattern = re.compile(alarmPreambleSynchIQPanel)
        patternMatch = re.findall(pattern,indata)  
        match_preamble(pattern, patternMatch, indata, hexname, fdir, capdir, processdir, origdir, select_process_mode, count_waterfall, alarm_num, alarmType, logflag)

def waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap):
    auto_logger.debug("Count Waterfall is %s and Alarm number is %s", count_waterfall, alarm_num)
    if (count_waterfall == alarm_num):
        remove_cap_file(alarmType, rmcap)
    else:
        auto_logger.debug("Processed as %s. No signal found.", alarmType)

def remove_cap_file(alarmType, rmcap):
    auto_logger.debug("Processed as "+alarmType+". No signal found.")
    delete_file(rmcap)
    auto_logger.debug("Removed .cap file : %s", rmcap)

def delete_nonalarm_files(sourcedir, delname, select_process_mode, count_waterfall, alarm_num, alarmType):

    auto_logger.debug("Remove all .txt files")
    auto_logger.debug("--------------------------------")
    auto_logger.debug("--------------------------------")

    # Remove .txt file that does not have any recognisable Alarm signals in it
    if delname.endswith(".dat.txt"):
        delete_file(delname)
        auto_logger.debug("Removed file : %s", delname)

    rmname = delname.rsplit("/", 1)
    rmcapname = rmname[1].split('_AddConst', 1)

# Check directory for other filenames that are the same as current file being processed
# If any files still present in the directory, that have a different offset, then keep .cap file
    constfile_list = []
    constname = []
    count_txt_files = 0
    if os.listdir(sourcedir):
        constfiles = [f for f in os.listdir(sourcedir) if not f.startswith('Capture_init')]
        constfiles_count = []
        for constfile in constfiles:
            # Check filename without Offset
            if "_AddConst" in constfile:
                constname = constfile.split('_AddConst', 1)
                count_txt_files += 1
        
        if count_txt_files == 0:           

        # Only remove .cap file if all, Alarm signal _AddConst files, have been processed and it's the last file with no signals in it
            rmcap = sourcedir+"/"+rmcapname[0]
            # auto_logger.debug("Remove file name: %s", rmcap)

            if (select_process_mode == 1) or (select_process_mode == 2):
                if (alarmType == "Spectra4000") and (os.path.isfile(rmcap)):
                    remove_cap_file(alarmType, rmcap)
                elif (alarmType == "YaleStandard") and (os.path.isfile(rmcap)):
                    remove_cap_file(alarmType, rmcap)
                elif (alarmType == "DSCAlexxor") and (os.path.isfile(rmcap)):
                    remove_cap_file(alarmType, rmcap)
                elif (alarmType == "Bosch3000") and (os.path.isfile(rmcap)):
                    remove_cap_file(alarmType, rmcap)
                elif (alarmType == "IQPanel") and (os.path.isfile(rmcap)):
                    remove_cap_file(alarmType, rmcap)

            if select_process_mode == 3:
                # In waterfall mode, the signal is checked as a Spectra signal first, then checked as a Yale signal, then as a DSC, then as a Bosch, then, if no signal found, remove the original .cap capture file
                if alarmType == "Spectra4000":
                    waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap)

                elif alarmType == "YaleStandard":
                    waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap) 

                elif alarmType == "DSCAlexxor":
                    waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap) 

                elif alarmType == "Bosch3000":
                    waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap)

                elif alarmType == "IQPanel":
                    waterfall_mode_msg(count_waterfall, alarmType, alarm_num, rmcap)

def delete_file(fName):
    if os.path.isfile(fName):
        try:
            os.remove(fName)
        except OSError, e:
            auto_logger.debug("Error: %s - %s. Cannot delete file" ,e.fName, e.stderror, exc_info=True)

def move_alarm_signals(source, destination, hexname, fdir):

    mvname = hexname.rsplit("/", 1)

    if destination.endswith("Original"):
        capname = mvname[1].split('_AddConst', 1)
        srcname = source+"/"+capname[0]
        dstname = destination+"/"+capname[0]
        if os.path.isfile(srcname):
            move_file(srcname,dstname, fdir)

    elif destination.endswith("Processed"):
        srcname = source+"/"+mvname[1]
        dstname = destination+"/"+mvname[1]
        move_file(srcname,dstname,fdir)

def move_file(sourceFile, destinationFile, fdir):
   # Before moving any files, check the location for sufficient space > 40 GB
    diskspace = int(check_disk_space(fdir)) 
    #auto_logger.debug(diskspace)
    if diskspace > 40000000:
        try:
           shutil.move(sourceFile,destinationFile)
        except shutil.Error as e:
           auto_logger.debug("Error: %s",e,exc_info=True)
        except IOError as e:
           auto_logger.debug("Error: %s",e.strerror,exc_info=True)
    else:
       auto_logger.debug("WARNING: Not enough disk space left where %s file is located.", destinationFile)

def check_disk_space(sourceFile):

    # Hard drive space is already checked when the GnuRadio capture and processing flowgraphs are run
    # This is an additional space check

    df = subprocess.Popen(["df", sourceFile], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
    out = output.split("\n")[1].split()
   # Disk free Space left
    return out[3]
