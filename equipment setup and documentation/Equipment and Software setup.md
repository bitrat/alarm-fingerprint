#EQUIPMENT AND SOFTWARE SETUP

1.	Base linux used: Ubuntu 16.04 (encrypted home directory caused an issue, so use a test PC and don't encrypt home dir)
2.	Install git

    $sudo apt-get install git –y

3.	Hackrf software install, test capture and replay
    
    https://mborgerson.com/getting-started-with-the-hackrf-one-on-ubuntu-14-04
    $ sudo apt-get install build-essential \
                       * cmake \
                       * libusb-1.0-0-dev \
                       * liblog4cpp5-dev \
                       * libboost-dev \
                       * libboost-system-dev \
                       * libboost-thread-dev \
                       * libboost-program-options-dev \
                       * swig

    $ git clone https://github.com/mossmann/hackrf.git

    Move to the hackrf/host directory.
    $ cd hackrf/host

    Create the build directory, move to it, and use Cmake (installed earlier) to create the Makefiles required for building.
    $ mkdir build && cd build
    $ cmake ../ -DINSTALL_UDEV_RULES=ON

    Build and Install.
    $ make
    $ sudo make install
    $ sudo ldconfig

    Test hackrf works:
    $hackrf_info

4.	Gnuradio software install
    https://github.com/mossmann/hackrf/wiki/Installing-gnuradio-on-Ubuntu-14.04-with-the-packaging-manager 

    $sudo add-apt-repository ppa:gqrx/releases
    $sudo apt-get update
    $sudo apt-get upgrade -y
    $sudo apt-get install gqrx gnuradio gr-osmosdr –y

    To run: $gnuradio-companion
    (Note: If gr-osmosdr Block missing in GnuRadio after install – reinstall it. Install gnuradio-dev. Install libhackrf-dev. Install gr-osmosdr to get osmocom source in gnuradio-companion (install 2 dependencies))

5.	Audacity install

    $sudo apt-get install audacity –y
    To run: $audacity

6.	Check python installed – yes 

7.	Install Don Weber’s python bitarray 0.8.1 and then grc_bit_converter.py

    $wget https://pypi.python.org/packages/source/b/bitarray/bitarray-0.8.1.tar.gz
    $ tar xzf bitarray-0.8.1.tar.gz
    $ cd bitarray-0.8.1
    $ sudo python setup.py install

    https://github.com/cutaway/grc_bit_converter 

    $git clone https://github.com/cutaway/grc_bit_converter.git

    Edited the grc_bit_converter.py file to write out a .txt file with hex values (which then gets processed further by process_signals.py file).
 
8.	Clone this repo  $ git clone https://github.com/bitrat/alarm-fingerprint.git 
9.	Change all references to "user" (directory and within .grc and .py files), to your ubuntu user name /home/user = /home/yourUser
9.	Create Alarm signal processing directory structure, on an external hard drive (if used)

##EXTERNAL Hard Drive
/media/user/SDRAlarmSignals/conf
/media/user/SDRAlarmSignals/Captured
/media/user/AlarmGnuradioFiles/AlarmSignals/logs
/media/user/GnuradioFiles/AlarmSignals/Original
/media/user/GnuradioFiles/AlarmSignals/Processed

10.	Test the capture_signals.py and process alarm python scripts.
chmod them all
scripts to contain #!usr/bin/env python or #!/bin/bash 

11.	 Espeak 
(to alert you when capture files all processed (indicates hackrf disconnected))
$ sudo apt-get install espeak

espeak_text.py contains:

\#!/usr/bin/env python
import subprocess

text = "Check if your capture device is still recording !"
subprocess.Popen(["espeak", "-v", "mb-en1", text])
time.sleep(5)

12.	Because normal Control+Z, Control+C in terminal does not kill the run_capture_flowgraphs script when it’s running:

$nano stop_run_capture_flowgraphs.sh
\#!/ bin/bash
killall run_capture_flowgraph_433920000_external
killall run_capture_flowgraph_433920000_local
killall run_capture_flowgraph_434320000_external
killall run_capture_flowgraph_434320000_local
killall timeout 30s
killall python puresignal_435720000MHz.py
killall python puresignal_435720000MHz_external.py
killall python puresignal_434320000MHz.py
killall python puresignal_434320000MHz_external.py

Attach it to a keyboard shortcut (Keyboard - Keyboard shortcuts - bash /home/bear/AlarmGnuRadioFiles/stop_run_capture_flowgraphs.sh)
$chmod u+x stop_run_capture_flowgraphs.sh
Assign Control+Alt+X shortcut.

Pressing Control+Alt+X when capturing signals stops capture loop and flowgraph.

##SUMMARY
Folder Directory Structure and Scripts within /home/user/alarm-fingerprint/AlarmGnuradioFiles
*	AlarmSignals
    *	logs
*	Original
*	Processed
    *	Captured
    *	Conf
    *	init

#Scripts
alarm_fingerprint.py
Bosch3000_FileInput_To_BinarySlice_Local_and_External.py
Bosch3000_FileInput_To_BinarySlice_Local_only.py
Capture_init.cap
capture_signals.py
DSC_FileInput_To_BinarySlice_Local_and_External.py
DSC_FileInput_To_BinarySlice_Local_only.py
IQPanel_FileInput_To_BinarySlice_Local_and_External.py
IQPanel_FileInput_To_BinarySlice_Local_only.py
grc_bit_converter.py
process_alarm_hex_auto.py
process_signals.py
puresignal_434320000MHz.py
puresignal_434320000MHz_external.py
puresignal_435720000MHz.py
puresignal_435720000MHz_external.py
run_addconst_flowgraphs
run_capture_flowgraph_433920000_external
run_capture_flowgraph_433920000_local
run_capture_flowgraph_434320000_external
run_capture_flowgraph_434320000_local
Spectra_FileInput_To_BinarySlice_Local_and_External.py
Spectra_FileInput_To_BinarySlice_Local_only.py
Stop_run_capture_flowgraphs.sh
Yale_FileInput_To_BinarySlice_Local_and_External.py
Yale_FileInput_To_BinarySlice_Local_only.py





