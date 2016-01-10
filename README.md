# alarm-fingerprint
code to blackbox fingerprint wireless alarm device signals

Being able to capture and replay wireless alarm signals can easily be done in a Lab environment, where it is known what is being triggered and when.

In a field/real world setting however, this is not so easy. A way of being able to capture signals, then identify if they are actually signals of interest, and store only those that are really wireless alarm peripheral signals, is necessary.

This project contains proof of concept code, which automates blackbox wireless alarm signal identification and storage.

GENERAL DESCRIPTION FOR RUNNING THE CODE

(Refer to Equipment setup documentation for how to glue this all together = hardware + software)

Create the AlarmGnuradioFiles folder in your user directory. Place scripts in this directory.

Create the following subdirectories:

- AlarmGnuRadioFiles
   - AlarmSignals
     - logs
     - Original
     - Processed
  - Captured
  - conf
  - init
  
The following is a description of the current python files, GNURadio files and order of processing (described for the DSC Alexor alarm, processed on local PC hard drive).

Scripts overview Example – DSC Alexor alarm, local drive

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

Process signal description

process_signals.py – select signal processing options from menu. looks in directory for .cap files (captured files) and passes them to :
- run_addconst_flowgraphs script, which will run the .cap files through different offsets (-0.25 to -0.9 in -0.05 steps using
- DSC_FileInput_To_BinarySlice_Local_only.py, which processes .cap captured signal file into Binary Sliced values (4DSC_SampSym file for processing further)
- Use Don Weber’s grc_bit_converter.py file (process signal into hex values).
- process_alarm_hex_auto.py (detects alarm signal preamble)
  - alarm_fingerprint.py (detects alarm signal content)

Captured signals files are processed from the Captured directory. If an alarm signal is positively identified:

- Moves .cap original captured signal file into AlarmSignals/Original directory.
- Moves .dat processed signal file into AlarmSignals/Processed directory. (Optional)
- Creates log file, in AlarmSignals/logs directory, to record what alarm, alarm peripheral signal captured.
