# alarm-fingerprint
code to blackbox fingerprint wireless alarm device signals

Being able to capture and replay wireless alarm signals can easily be done in a Lab environment, where it is known what is being triggered and when.

In a field/real world setting however, this is not so easy. A way of being able to capture signals, then identify if they are actually signals of interest, and store only those that are really wireless alarm peripheral signals that are useful for replay, is necessary.

This project contains proof of concept code, which automates blackbox wireless alarm signal identification and storage (useful for  later replay).

## Alarm components:
- Spectra 4000 with both RX1 and RTX3 wireless modules, DCT2 reeds, PMD75 PIR, REM15 and REM3 keyfobs.
- DSC Alexor wireless alarm system,WS4945A reeds, WS4904 PIR and WS4939 keyfobs.
- Bosch 3000 with B810 wireless module, RFDW-SM reeds, RF940E PIR and RFKF-FB keyfobs.
- Yale standard wireless alarm system.
- IQPanel alarm system (Cinch Reeds and IQMotion PIRs) - Marketed under other names (with fairly Hostile to research T&C's).

Test alarm signals (to verify processing code has been setup up correctly, can be downloaded from https://drive.google.com/folderview?id=0B8gCZryoEOWIZDBsbVFVZF93dW8&usp=sharing ).

These .cap files must be placed in the Captured folder (within the home\user\alarm-fingerprint\AlarmGnuRadioFiles Folder structure)

## GENERAL DESCRIPTION FOR RUNNING THE CODE

(Refer to [Equipment setup documentation](https://github.com/bitrat/alarm-fingerprint/blob/master/equipment%20setup%20and%20documentation/Equipment%20and%20Software%20setup.md) for how to glue this all together = hardware + software)

The scripts are run within the home/user/alarm-fingerprint/AlarmGnuradioFiles folder. Replace "user", in the scripts, with your home directory username. Any external harddrive is referenced as /media/user in the scripts, change to your path/username.
  
The following is a description of the current python scripts, GNURadio files, and the order of processing (The Example described, is for the DSC Alexor alarm, processed on local PC hard drive).

### Scripts overview Example – DSC Alexor alarm, local drive

./capture_signals.py

./ process_signals.py 
   - run_addconst_flowgraphs 
   - DSC_FileInput_To_BinarySlice_Local_only.py 
   - grc_bit_converter.py 
   - process_alarm_hex_auto.py 
   - alarm_fingerprint.py

Capture signal – Example DSC Alexor signals onto Local harddrive

capture_signals.py – select signal capture options from menu.
  - starts run_capture_flowgraph_433920000_local script
  - runs puresignal_435720000MHz.py flowgraph, captures signals every 30 seconds, saves .cap files into a directory.
Note: Needed to use timeout in run_capture_flowgraph_433920000_local script at the moment ,because wait() and stop() didn't work in .grc flowgraph code. (Could possibly do this with GnuRadio Block message passing). 

###Process signal description

process_signals.py – select signal processing options from menu. looks in directory for .cap files (captured files) and passes them to :
- run_addconst_flowgraphs script, which will run the .cap files through different offsets (-0.25 to -0.9 in -0.05 steps). Uses .py file :
- DSC_FileInput_To_BinarySlice_Local_only.py, which processes .cap captured signal file into Binary Sliced values (4DSC_SampSym file for processing further)
- Use Don Weber’s grc_bit_converter.py file (process signal into hex values).
- process_alarm_hex_auto.py (detects alarm signal preamble)
  - alarm_fingerprint.py (detects alarm signal content)

Captured signals files are processed from the Captured directory. If an alarm signal is positively identified:

- Moves .cap original captured signal file into AlarmSignals/Original directory.
- Moves .dat processed signal file into AlarmSignals/Processed directory. (Optional)
- Creates log file, in AlarmSignals/logs directory, to record what alarm, alarm peripheral signal captured.

#TO DO
* SIGINT - Process date and time of the peripherals and keyfobs to track occupants movements/presence
* REM3 keyfob signal is detected - but process further to determine actual State - Lock, Unlock etc (like other alarm peripherals)
* Transform the .doc files (that currently have to be downloaded to be read) into proper text with graphics to be displayed here.
* Rewrite this POC tool and Package it properly (will probably never happen)
