#Spectra 4000 wireless peripherals (RX 1 and RTX3 wireless modules)
Wire RTX3 up to the Spectra 4000.
Note: RTX3 will only work in one way mode with Spectra 4000, there is scope to test SP versions higher, with 2 way mode.
For the REM3 Keyfob you must have RTX3 wired up.
(One way to Program remotes, Pg 35/36 of the Spectra manual.)
##UPDATE (What the Keyfob and code settings are currently): 
Master code is 2345.
Installer code is 0000.
Codes are currently set to 4 digit codes: 
REM15Kf1 is user 1, code 2345 (user 1 = MC).
REM3 KF1 is user 2, code 1111.
REM15Kf2 is user 3, code 7890.
REM3 KF2 is user 4, code 6852.
REM3 KF3 is user 5, code 7744.

Program a new REM3 (example):
Location [655] is RC for user 5.In the experiment, user 5 is REM3 Keyfob 3, Serial number: 227108. Code for user changes to view different signals. 7744.
To reprogram REM3 with 7744 code as user 5. Note: Always wait for beeps between the following steps:
Power key. 2345 (master code = user 1)
05 (User number)
7744
7744
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Arm Spectra (press and hold ARM button) and then Test Disarming with new code 7744 on REM3 (Press I, then OFF, then 7744).

To check Serial number of remotes at any stage:
Press ENTER, 0000 (wait for beeps)
651 (Remote 1 programming location - wait for beeps)
ENTER, ENTER ... to step through serial number(s).
Clear, Clear

##Capture and replay one Touch and entering codes on REM3
On your Linux computer (where GNURadio and the alarm-fingerprint code is),:
$cd alarm-fingerprint
$./capture_signals.py
Set and unset the alarm with the remote you are wanting to test (and eventually ID).
After capturing, process the signals to see whether the code fingerprints them properly (test).

##Program User 2
Power key. 2345 (master code = user 1)
02 (User number)
2345
2345
Press i on remote (then press i again), wait for confirmation. 
Clear, clear, clear.

To arm, press i, then long press ARM until yellow transmit flashes.
To ARM using code, press i, then press 2345 (user code 2 programmed to be the user for the REM 3.
To disarm, press i, then press OFF, then press 2345 (user code 2 programmed for REM 3).

You can enable One Touch arming on the REM 3.
The default however is to require code entry on the REM 3 to arm.

##Experiment:
Open gnuradio-companion.
RTL-SDR Source set at 434.165MHz to shift DC spike away from 433.92MHz.
Arm and disarm with code.
Find out transmission frequency, it says 433 MHz. Transmission confirmed as 433.92MHz.

###Use HackRF
Capture and replay signals at the frequency. If no easy replay possible, try different sample rates, LNA gain and VGA gain and frequencies.

###Open signal in Audacity.
$audacity
File - Import - Raw data - Signed 8 bit PCM, no endianness, Mono, 10000Hz (decimated)
Look at LockOneTouch, versus Lock Code. Unlock Code.

Not every signal captured is an ideal one.

Capture all number code combinations and open in Audacity. For example 1111 to 9999 etc. 
Try and ascertain a pattern.

###RTX3, 4 digit codes base, 2 REM3 keyfobs, capture and replay
Look at GQRX waterfall, identify what frequency REM3 keyfobs transmit at. = 433.92MHz.
REM Keyfob 1 serial number is: 240236.
REM Keyfob 2 serial number is: 241179.

For each REM3 keyfob, capture several Lock signals, Unlock signals, Stay arm signals and Sleep signals using hackrf_transfer commandline function.
i.e. for Lock signals for REM3 Keyfob 1, capture file naming convention with hackrf_transfer is:
$ hackrf_transfer –a 1 –f 433920000 –r REM3KF1Lock1_43392

If alarm does not respond on first hackrf_transfer –t, then need to use .\Replay.sh looping function – replay loop 40 times and see on which loop, the alarm responds (if at all – if no response after 40 replays, then it’s Loop x)

REM3KF1Lock1_43392
xLoop 40
xLoop 40
REM3KF1Lock2_43392
xLoop 40
xLoop 40
REM3KF1Lock3_43392
Loop 1
REM3KF1Lock4_43392
Loop 1
REM3KF1Sleep1_43392
Loop 17
REM3KF1Sleep2_43392
xLoop 40
REM3KF1Stay1_43392
xLoop 40
REM3KF1Stay2_43392
Loop 4

REM3KF1Unlock1_43392
xLoop 40
xLoop 40
REM3KF1Unlock2_43392
xLoop 40
xLoop 40
REM3KF1Unlock3_43392
xLoop 40
xLoop 40
REM3KF1Unlock4_43392
xLoop 40
REM3KF1Unlock5_43392
xLoop 40
REM3KF1Unlock6_43392
xLoop 40
REM3KF1Unlock7_43392
xLoop 40
REM3KF1Unlock8_43392
xLoop 40

REM3KF2Lock1_43392
Loop 1
Loop 1
Loop 1
Loop 1
REM3KF2Lock2_43392
Loop1
REM3KF2Sleep1_43392
Loop 1
REM3KF2Sleep2_43392
Loop 1
REM3KF2Stay1_43392
Loop 1
REM3KF2Stay2_43392
Loop 1

REM3KF2Unlock1_43392
Loop1
Loop 4
(Sleep) xLoop 40
Loop 2
REM3KF2Unlock2_43392
Loop 2
REM3KF2Unlock3_43392
(Sleep) xLoop 40 
REM3KF2Unlock4_43392
(Stay) xLoop 40 
REM3KF2Unlock5_43392
(Stay) xLoop 40
REM3KF2Unlock6_43392
(Lock) xLoop 40

REM3KF1Lock1_434165
Loop 1
REM3KF1Unlock1_434165
Loop 1 (Lock)
Loop 1 (Stay)
REM3KF1Sleep1_434165
Loop 2
REM3KF1Stay1_434165
Loop 1
REM3KF1Unlock2_434165
Loop 1
REM3KF1Unlock3_434165
xLoop 40

REM3KF2Lock1_434165
Loop 1
REM3KF2Unlock1_434165
Loop 1 (Lock)
xLoop 40 (Stay)
xLoop40  (Lock)
REM3KF2Sleep1_434165
xLoop 40
xLoop 40
REM3KF2Stay1_434165
Loop 1
Loop 1
REM3KF2Unlock2_434165
xLoop 40 (Stay)
REM3KF2Unlock3_434165
xLoop 40 (Stay)

Much better when capturing signals offcentre at the 434.165 MHz.

Capture some signals at 434.65 MHz and some at 433.92 MHz. Test if replay results are better if the signals are captured off-centre (from 433.92 MHz)?
Compare REM3 keyfob signals per button – Identify similarities. Identify button-type bits. Identify unique Keyfob bits.
Compare REM3 Keyfob signals to the REM15 keyfobs.

Import Raw – Signed 8 Bit PCM – No endianness – Mono – start offset 0 – 10,000,000 Hz.
Compare REM3KF1Lock1_43392 and REM3KF2Lock1_43392.

###RTX3, 4 digit codes capture and replay
Set usercodes to be 6 digit.(When going from 4 digit to 6, the first 2 digits of the 4 digit code are added to the end, i.e 2345 becomes 234523)
ENTER 0000
701 (Option 1 OFF = 6 digit code) , ENTER
Clear, clear.

All keyfobs work as is, with the new 6 digit codes.

Capture and replay 6 digit codes, look at them in Audacity and compare with 4 digit captured signal of similar codes i.e compare 2345 signal to 234523 signal. 

###RTX3, 6 digit codes capture and replay
- Difference in user number/code signal sent between REM3 and REM15 keyfobs ?
Set usercodes 1 to 3 (keyfobs are assigned to users 1 to 3) and register the 3 keyfobs.
To find out which user has been assigned which keyfob, check Manual Pg 36.
Location [651] is RC for user 1. In the experiment, user 1 is REM15 Keyfob 1, Serial number: 020226. Code for user 1 to be: 234523 (System Master Code).

First time programming of REM15 Keyfob 1 as user 1, MC is 123412. Change to 234523.
Power key. 123412 (master code = user 1)
01 (User number)
234523
234523
press any REM15 Keyfob 1 remote button twice (1 second between presses)
clear, clear.

To check serial number of keyfobs at any stage,
Press ENTER, 000000 (wait for beeps)
651 (wait for beeps)
ENTER, ENTER ... to step through serial number(s).
Clear, Clear

Location [652] is RC for user 2.In the experiment, user 2 is REM3 Keyfob 2, Serial number: 240236. Code for user changes to view different signals. 111111.
To reprogram REM3 with 111111 code as user 2.
Power key. 234523 (master code = user 1)
02 (User number)
111111
111111
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Test Disarming with new code 111111.

Location [653] is RC for user 3.In the experiment, user 3 is REM15 Keyfob 2, Serial number: 085213. Code for user is: 345634.
Set code for user 3, Power+ MC(234523)
user number, 03
345634
345634
press any REM15 Keyfob 2 remote button twice (1 second between presses)
clear, clear.

###RTX3, 6 digit codes base, 3 keyfobs, capture and replay - Current state
Weird thing, dropping power to the panel seemed to affect 

For Kf1 and Kf2 
Loop = REM15LockOne Signal
Loop = REM15UnlockOneSignal

REM15Kf1Lock1_43392
Loop 1
Loop 2
Loop 1
Loop 1
REM15Kf1Lock2_43392
xLoop 40
xLoop 40
xLoop 40
xLoop 40
REM15Kf1Unlock1_43392
Loop 
Loop
Loop
Loop
REM15Kf1Unlock2_43392
Loop 1
Loop 1
Loop 1
Loop 1

REM15Kf2Lock1_43392
xLoop 40
xLoop 40
xLoop 40
xLoop 40
REM15Kf2Lock2_43392
xLoop 40
xLoop 40
xLoop 40
xLoop 40
REM15Kf2Lock3_43392
xLoop 40
Loop 
Loop 
Loop 
REM15Kf2Unlock1_43392
xLoop 40
xLoop 40
xLoop 40
Loop
REM15Kf2Unlock2_43392
xLoop 40
xLoop 40
Loop
Loop

Loop = REM3LockOneSignal
Loop = REM3UnlockOneSignal

REM3Lock1_43392
Loop 9
Loop 1
xLoop 40
xLoop 40
xLoop 40
xLoop 40
** 20 minute break, test if Interference with heartbeat signal not the cause of sudden no lock/unlock.
xLoop 40
Loop 22


REM3Lock2_43392
Loop 2
Loop 1
Loop 1
Loop 1
REM3Unlock1_43392
xLoop 40
Restarted alarm Panel, tested Locking with REM3Lock2_43392 signal
xLoop 40
xLoop 40
xLoop 40
xLoop 40
xLoop 40


REM3Unlock2_43392
xLoop 40
xLoop 40
xLoop 40
wait 20 minutes, to Test if heartbeat needs to be identified to make unlock work better.
xLoop 40
xLoop 40
xLoop 40

REM3Unlock3_43392
xLoop 40
xLoop 40
Restarted alarm Panel, tested Locking with REM3Lock2_43392 signal
xLoop 40
xLoop 40


###4 and 6 codes, capture and replay
Working signals - only work, if you haven't messed with the codes in the system
REM3Lock1oneTouch_43392
REM3Lock2oneTouch_43392
REM3Lock1oneTouchCode1111_43392
REM3Unlock1Code1111_43392
Loop 1
REM3Lock1oneTouchCode2222_43392
REM3Lock1oneTouchCode3333_43392
REM3Unlock1Code3333_43392
REM3Lock1oneTouchCode4444_43392
REM3Lock1oneTouchCode5555_43392
REM3Lock1oneTouchCode1234_43392 (had to capture a second time for it to work well)
REM3Unlock1Code5555_43392
REM3Unlock1Code1234_43392
REM3Unlock1Code111111_43392 (second signal capture, first loop)
REM3Lock1oneTouchCode1111_43392 (second signal capture, second loop)

####6 code signals
REM15Kf1Lock1Code234523_43392
x REM15Kf1Unlock1Code234523_43392
x REM15Kf2Unlock1Code345634_43392
x REM15Kf2Lock1Code345634_43392

####Audacity project
REM3Unlock1Code2345_43392
REM3Unlock1Code2222_43392
REM3Unlock1Code3333_43392
REM3Unlock1Code4444_43392
REM3Unlock1Code5555_43392

Changed user 2 REM3 code to 1111 code, replay a previous working captured 1111 Unlock code. Didn't work at first, then it did work. Captured another REM3Unlock2Code1111_43392 signal. 

##DCT2 Ultra small Door Contact (Reed 1) with RTX3
Serial number: 214097

Installation on a Spectra 4000. Works with the RTX3 and detected by RX1.
Open the larger of the 2 door contact units, insert coin cell battery.

Check-in supervision time is set in the control panel.

Assign the Door Contact to a Zone. Pg 19 Installer manual, Wireless zone assignment.
Wireless, Zone 2, is in programming location 062. Enter the serial number of the Door Contact. 

Enter, 000000
062
214097
Clear, clear.

In Zone definition, make Zone 2 Instant.
Enter, 000000 (installer code and codes were set to 6 digit for this experiment)
002 (Zone number)
08 (Instant zone type)
1 (Partition)
Enter
Clear, clear.

Tested door contact causes an alarm when triggered, when alarm is set.

Capture door contact open signal using the HackRF:
hackrf_transfer -a 1 - f 433920000 -r SpectraDoorContact1_Open1_Unset_43392

Worked first time replay: 
SpectraDoorContact1_Open1_Set_43392
Loop 1 (no restore)
Loop 1
Loop 2
Loop 3
Loop 1
Loop 1

SpectraDoorContact1_Close1_Set_43392
(Loop = SpectraDoorContactOpenLoop)
Loop 1
Loop 13
Loop 4
xLoop 40
Loop 2
xLoop 40
Loop 32
Loop 3
xLoop 40
xLoop 40
Loop 3

SpectraDoorContact1_Close1_Unset_43392
(Loop = SpectraDoorContactCloseLoop)
Loop 1
Loop 3
xLoop 40
Loop 1
Loop 3
Loop 1
Loop 7
Loop 4

Worked after multiple replays (3+)
SpectraDoorContact1_Open1_Unset_43392
Loop 3
Loop 32
Loop 21
Loop 1
Loop 5
Loop 2
Loop 2
Loop 1

##PMD75 PIR with RTX3
Serial number: 154245

Installation on a Spectra 4000. Works with the RTX3 and detected by RX1.
Open the PIR, insert 3 AAA batteries and pin onto circuit board.

Check-in supervision time is set in the control panel.

Assign the PIR to a Zone. Pg 19 Installer manual, Wireless zone assignment.
Wireless, Zone 5, is in programming location 065. Enter the serial number of the PIR. 
Enter, 000000
065
154245
Clear, clear.

In Zone definition, make Zone 5 Instant.
Enter, 000000 (installer code and codes were set to 6 digit for this experiment)
005
08
1
Enter
Clear, clear.

Tested PIR causes an alarm when triggered, when alarm is set.
Wait 3 minutes after setting PIR in alarm (it goes into Energy Save mode after 2 alarm activations within 5 minutes, LED still works on PIR, but no further activations sent for 3 minutes).

Capture PIR open signal using the HackRF:
hackrf_transfer -a 1 - f 433920000 -r SpectraPIR1_Open1_Unset_43392
Loop 1 (PIR signal restores)
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 2
RX1 - Loop 2

Worked after multiple replays (2+)
hackrf_transfer -a 1 - f 433920000 -r SpectraPIR1_Open2_Unset_43392
(Loop = SpectraPIROpenLoop)
Loop 2
xLoop 40
Loop 16
xLoop 40
Loop 13
Loop 15
Loop 9
Loop 1
Loop 1
Loop 3

Didn't seem to work well (Test longer loops, 30+, with Alarm set):
hackrf_transfer -a 1 - f 433920000 -r SpectraPIR1_Open1_Set_43392
Loop 3
Loop 2
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 1
RX1 - Loop 1
Loop 
Loop

hackrf_transfer -a 1 - f 433920000 -r SpectraPIR1_Open2_Set_43392
xLoop 40
xLoop 40
RX1 - Loop 10
RX1 - Loop 7
RX1 - Loop 7
RX1 - Loop 5
Loop 
Loop 

##DCT2 Ultra small Door Contact (Reed 1) with RX1
Serial number: 214097

Tested door contact causes an alarm when triggered, when alarm is set.

Capture door contact open signal using the HackRF:
hackrf_transfer -a 1 - f 433920000 -r RX1SpectraDoorContact1_Open1_Unset_43392

Replay Attack attempts
(Loop = SpectraDoorContactOpenLoop)
RX1SpectraDoorContact1_Open1_Set_43392
Loop 1 (no restore)
Loop 1
Loop 4
xLoop 40
xLoop 40
xLoop 40
Loop 13
Loop 2
Loop 33

RX1SpectraDoorContact1_Close1_Set_43392
(Loop = SpectraDoorContactOpenLoop)
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1

RX1SpectraDoorContact1_Open1_Unset_43392
Loop 1
Loop 1
Loop 1
Loop 1
Loop 2
Loop 1
Loop 1
Loop 1

RX1SpectraDoorContact1_Close1_Unset_43392
(Loop = SpectraDoorContactCloseLoop)
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1

##PMD75 PIR with RX1
Serial number: 154245
Wired up RX1 where RTX3 previously was. Works with RX1 but replay was tricky with originally captured signals.

Tested PIR causes an alarm when triggered, when alarm is set.
Wait 3 minutes after setting PIR in alarm (it goes into Energy Save mode after 2 alarm activations within 5 minutes, LED still works on PIR, but no further activations sent for 3 minutes).

Capture PIR open signal using the HackRF:
hackrf_transfer -a 1 - f 433920000 -r RX1SpectraPIR1_Open1_Unset_43392
(Loop = SpectraPIROpenLoop)
xLoop 40
xLoop 40
Loop 32
xLoop 40
Loop 12
xLoop 40
xLoop 40
xLoop 40

hackrf_transfer -a 1 - f 433920000 -r RX1SpectraPIR1_Open2_Unset_43392
xLoop 40
xLoop 40
xLoop 40
xLoop 40
Loop 13
xLoop 40
xLoop 40
xLoop 40

hackrf_transfer -a 1 - f 433920000 -r RX1SpectraPIR1_Open1_Set_43392
Loop 2
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1
Loop 1

hackrf_transfer -a 1 - f 433920000 -r RX1SpectraPIR1_Open2_Set_43392
xLoop 40
xLoop 40
xLoop 40
Loop 38
Loop 18
Loop 27
Loop 21
Loop 11
Cannot Test RX 1 with RX 3 Antenna - soldered on to board

##Audacity comparison images
Signed 8bit PCM, no endianness, 10000Hz (decimated as sample rate is 10M) 
SDR Research signals and temp on Backup drive.

SDR Research Aug 4 folder on Seagate drive. RX1 = Spectra signals.

##On Linux computer
Compare 10000 Hz signal to 10 M signal. Audacity project - Spectra10MTimingREM3.
REM3UnlockCode2345Compare_43392

Least Long signal = 25:54.1762 to 25:54.2171
Double Signal = 25:54.2958 to 25:54.3756 


Full signal = 25:49.2270 to 25:58.525 
Preamble = 25:49.2270 to 25:50.466 (preamble header then 13 blips ending on 0)
Synch word =  25:50.466 to 25:50.786 (0 synch word 0)
Data signal = 25:50.786 to approx. 25:58.526 (approx. because could have 3 zero signals after, depends where the last little blip starts)  (0 then data)

Compare REM15 and REM3 keyfob signals 
(Audacity project Spectra3KeyfobRTX3UnlockCompare43392) :
REM15Kf1Unlock2_43392
REM15Kf2Unlock1Code345634_43392
SpectraRTX3REM3UnlockTest_43392

(Audacity project Spectra3KeyfobRTX3LockCompare43392) :
SpectraRTX3Kf1UnlockTest_43392
SpectraRTX3Kf2UnlockTest_43392
SpectraRTX3REM3UnlockTest_43392

Is it the code that is assigned to the keyfob that makes the difference ?
Currently above signals are REM15 Kf1 is code 234523 (user 1)
REM15 Kf2 is code 345634 (user 3)
REM3 is code 111111 (user 2)

##Swap Keyfob users
Make REM15 Kf1 user 2 (code 111111)
Then make REM3 user 1 (code 234523 )

Location [651] is RC for user 1.In the experiment, user 1 becomes REM3 Keyfob, Serial number: 240236. Code for user is: 234523.
Set code for user 1, 
Power+ MC(234523)
user number, 01
234523
234523
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Test Disarming with new code 234523.

To reprogram REM15 Kf1 with 111111 code as user 2.
Power key. 234523 (master code = user 1)
02 (User number)
111111
111111
press any remote button twice.
clear, clear, clear


Capture hackrf signals for swapped Keyfob users+code, then compare to the signals captured earlier
SpectraRTX3Kf1LockTestSwap_43392
SpectraRTX3REM3LockTestSwap_43392

SpectraRTX3Kf1UnlockTestSwap_43392
SpectraRTX3REM3UnlockTestSwap_43392

###Both are user 1 (have code 234523)
Compare these pairs:
SpectraRTX3Kf1LockTest_43392
SpectraRTX3REM3LockTestSwap_43392 

SpectraRTX3Kf1UnlockTest_43392
SpectraRTX3REM3UnlockTestSwap_43392

SpectraRTX3Kf1LockTestSwap_43392
SpectraRTX3REM3LockTest_43392 

SpectraRTX3Kf1UnlockTestSwap_43392
SpectraRTX3REM3UnlockTest_43392

##Swap keyfob users Back 
(as they were at the start of the 6 code experiment)

Make REM15 Kf1 user 1 (code 234523 ) again.
Then make REM3 user 2 (code 111111) again.

Location [651] is RC for user 1.In the experiment, user 1 becomes REM15 Keyfob1, Serial number: 020226 again. Code for user 1 is: 234523.
Set code for user 1, 
Power+ MC(234523)
user number, 01
234523
234523
press any Keyfob 1 remote button twice (1 second between presses)
clear, clear.

To reprogram REM3 with 111111 code as user 2.
Power key. 234523 (master code = user 1)
02 (User number)
111111
111111
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Test Disarming with new code 111111.

##Audacity

Import raw - 32 bit float - no endianess - Mono - 0 start bit - 10,000,000 Hz

Preamble 
13 short
Long Synch word
Short and Long signals = data

Preamble Long High start       35:06.1585
Preamble Long High stop       35:06.324219

First Preamble low/high start          35:06.324219
First Preamble low stop high start  35:06.3652
First Preamble low/high stop          35:06.40606

13 total Preamble low/high
Last Preamble low/high start  35:07.30727
Last Preamble low/high stop  35:07.38910

zero break before synchword long high
Zero break start                      35:07.38910
Synch word start high             35:07.4762
Synch word stop high             35:07.7213
Zero break after synch start   35:07.7213
Zero break after synch stop   35:07.7994

Analyze Data - are there consistent high, low patterns.
There are 2 types of high signals (one short, one long)
Are these a combo of high and low ? = a total signal
Data short high = 100
Data long high  = 110

Randomly selected - to get an overview of the signal length

Data short high start   35:07.7994    1 = 0.0427
Data short high stop   35:07.8421    0 = 0.0401
Data short zero stop   35:07.9223    0 = 0.0401

Data long high start    35:07.9223     1 = 0.0414
Data long high stop    35:08.0051     1 = 0.0414
Data long zero stop    35:08.0450     0 = 0.0399

Data short high start   35:09.6425     1 = 0.0428
Data short high stop   35:09.6853     0 = 0.03995
Data short zero stop   35:09.7652     0 = 0.03995

Data long high start    35:10.6256      1 = 0.04145
Data long high stop    35:10.7085      1 = 0.04145
Data long zero stop    35:10.7484      0 = 0.0399

Sample rate = 10,000,000 Hz
Is a symbol a 0 or a 1 ? Or is a symbol the 100 and 110 ?
0   = 0.0400 
1   = 0.0428
11 = 0.0828

Calculations:
Single 0 or 1 symbol assumption, around 0.0400 seconds per symbol
Symbol rate = symbols per second
Sample rate = 10,000,000 Samples /second

0.0400 x 10,000,000 = 400,000 samples per symbol
Apply any decimation (100 or 250), changes samples per symbol to 4000.
Samples per symbol = Omega value in the Clock Recovery Module

samples/sec divided by samples /symbol = data rate

Three bits per symbol, around 0.1229 seconds per symbol.
Sample rate = 10,000,000 Samples /second

0.1229 x 10,000,000 = 1,229,000 samples per symbol
Apply any decimation (100), changes samples per symbol to 12290.
Samples per symbol = Omega value in the Clock Recovery Module

Compare single symbol and three bit symbol graphs after Clock Recovery Module
Single symbol works best, decimation 250 and symbol rate of 40,000

Use gnuradio flowgraph SpectraRTX3_FileInput_Reed1.grc
- Produced 4 files, 
- Used the 3Spectra_Reed1_SampSym file (opened in audacity) to look at LPF processed output.

##Processed .txt files
Preamble 1 long high
                 13 short zero then high
                  1 very long high
                  0's 
Data 33 same length symbols (either 100, or 110)
------------------
4Spectra_Reed1_SampSym.txt
7 lots of actual Reed 1 open signal, 1 Close signal:
first 3 are good, 4, preamble chopped, synch word present, 5 preamble is chopped, synch word still there, 6 is a write-off, 7 also a write-off, 8 is close signal good
x20 x00 x00 x00 x04 x10 x04 x08 x02 x28 x02 x08 x02 x84 x01 x04 x01 x04 x00 xaa x00 xa2 x00 x85 x00 x41 x00 x51 x00x20 x80 x20 x01 x40 x00 x00 x00 x00 x00

x0a x00 x20 x04 x00 x10 x00 x04 x10 x00 x02 x08 x00 x02 xa8 x00 x01 x54 x01 x40 x00 x00 xa0 x02 x00 x00 x55 x00 x00 x45 x00 x20 x00 x80 x20 x00 x80 x00 
....

7 lots of actual Reed 1 Open and then 5 Reed 1 close signals
first 3 open are good, all 5 Reed1 close signals good but very low compared to Open Reed 1 signals.
----------------------
Processed Reed 1 offset -0.02 (enough of an offset for the particular signal captured, anymore and the Close signals would have disappeared)

First 3 of 7 Open Reed 1 signals are good.
All 5 of 5 Close Reed 1 signals are good.

First Open Reed 1 signal part 1 analysis:

Preamble    Synchword      Data (33 symbols)
34 1's          16   0's            10  1's       10  1's       18  1's        9  1's
7   0's          50   1's            15  0's       15  0's        7   0's       15  0's
9   1's          15   0's
8   0's                                  17  1's       9   1's       18  1's       10  1's
9   1's                                   7   0's       15  0's       7   0's       15  0's
7   0's
9   1's                                  18  1's       18  1's       9   1's        9   1's
7   0's                                   7   0's       7    0's       15  0's       15  0's
9   1's
8   0's                                  17  1's       10  1's       18  1's       18  1's
9   1's                                   7    0's      15  0's        7   0's        7   0's
7   0's
9   1's                                  18  1's       17  1's       17  1's       18  1's
7   0's                                   7   0's       7    0's        7   0's        7   0's
10 1's
7   0's                                   9   1's       10  1's       17  1's        9   1's
9   1's                                  16  0's       15  0's        7  0's       15  0's
7   0's
9   1's                                   9   1's        9   1's       10  1's
8   0's                                  15  0's       15  0's       15  0's
9   1's
7   0's                                  18  1's       10  1's        9  1's
9   1's                                   7   0's       15  0's       15  0's
7   0's
10 1's                                  17  1's       15  1's       10  1's
7   0's                                   7   0's        7   0's       15  0's
9   1's

Reed 1 Open signal hex values add up to 34 1's:
0f ff ff ff fc
1f ff ff ff f8
3f ff ff ff f0
7f ff ff ff e0
ff ff ff ff c0

Reed 1 Close signal hex values add up to 33 1's
ff ff ff ff 80
01 ff ff ff ff
7f ff ff ff c0
3f ff ff ff e0
-------------------------
Processed Reed 2 offset -0.05 (-0.02 is not enough to deal with blips up past zero line, which will be interpreted as spurious 1 bits)

##Description of Reed signals processing

1.	Used ./run_capture_flowgraphs script to create Capture_2015.10.18.16.41.cap
2.	Put Capture_2015.10.18.16.41.cap file through the SpectraRTX3_FileInput_Reed2.grc flowgraph (at offset -0.05) to create 4 files at each stage of the processing into a binary sliced file.
3.	Look at the 3Spectra_Reed2_SampSym in audacity, it is the Clock Recovery block output file - check offset enables correct 0's and 1's to be detected, AND not too many of the Close Reed2 signals disappear. Open Reed 2 - 1 to 8 parts are good. Close Reed 2 - 1 to 8 parts are good.
4.	Process 4Spectra_Reed2_SampSym through the grc_bit_converter.py file to produce a .txt file with hex values.

Reed 2 Open preamble
0f ff ff ff fc   = 34 bits
3f ff ff ff f0   = 34 bits
ff ff ff ff c0   = 34 bits
07 ff ff ff ff   = 35 bits
07 ff ff ff fe  = 34 bits
7f ff ff ff f0   = 35 bits

Reed 2 Close preamble
07 ff ff ff fe  = 34 bits
0f ff ff ff f8   = 33 bits
ff ff ff ff c0   = 34 bits
07 ff ff ff ff   = 35 bits
3f ff ff ff f0   = 34 bits
01 ff ff ff ff d1 = 35 bits
03 ff ff ff ff   = 34 bits
0f ff ff ff fc   = 34 bits

Checked signal for status bits of  REM15  Keyfob 1 and 2, Dot 1 and Dot 2 default programming.
Programming guide Pg 34/35 Remote Control Button assignment
Dot 1 default programming is option B - PGM activation (event group 8)
Dot 2 default programming is option C - PGM activation (event group 8)

Check default programming on all keyfobs
Press ENTER, then 0000 (installer code), wait for beeps.
610              (All keyfobs programming location - if programming the same options for all keyfobs in the system)
ENTER        (Check current programming)
                     1         (option 1 regular arm/force arm)
ENTER
                     OFF    (option B)
ENTER
                     BYP    (option C)
ENTER
                     0         (option - Disarm, cannot reprogram)
Clear, clear.             (exit programming)

Reprogram Dot 1 as option 2 - stay/Force arming, and Dot 2 as option 4 - sleep arming:
Press ENTER, then 0000 (installer code), wait for beeps.
610              (All keyfobs programming location - if programming the same options for all keyfobs in the system)
                     1         (option 1 regular arm/force arm)

                     2    (option 2)

                     4    (option 4)

                     0         (option - Disarm, cannot reprogram)
keep pressing 0 until several beeps are heard.   (end of section)
Clear, clear.             (exit programming)
Import KF1 and Kf2 Dot 1 and Dot2 signals into audacity
32 bit float
Mono
no endianess
Start bit 0

SpectraPIR_Open1_Unset_43392
SpectraDoorContact1_Open1_Unset_43392
REM15Kf2Unlock3_43392
REM3Unlock1_43392

##REM3 Signals analysis

Audacity project for 4 code Unlock signals: SpectraREM3UnlockSignalsPart2 code 2345 1234 1212 5555

REM3Unlock1Code2345_43392
REM3Unlock1Code1234_43392
REM3Unlock1Code1212_43392
REM3Unlock1Code5555_43392
Audacity Project for comparing 4 code and 6 code unlock signals, make sure they are the same user (in this case user 2)
Capture:
REM3UnlockCode111111Compare_43392

Switch back to 4 digit code
ENTER 000000
701 (Option 1 ON = 4 digit code) , ENTER
Clear, clear.

Recalibrate REM3 keyfob to the user 2, 4 digit code:
Power key. 2345 (master code = user 1)
02 (User number)
1111
1111
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Test Disarming with new code 1111.

Capture:
REM3UnlockCode1111Compare_43392

Switch back to 6 digit code
ENTER 0000
701 (Option 1 OFF = 6 digit code) , ENTER
Clear, clear.

Recalibrate REM3 keyfob to the user 2, 6 digit code:
Power key. 234523 (master code = user 1)
02 (User number)
111111
111111
Press i on remote, wait for confirmation beep. 
Clear, clear, clear.
Test Disarming with new code 111111.


In Audacity Project SpectraREM3_4digitCode6digitCode compare 
REM3UnlockCode111111Compare_43392
REM3UnlockCode1111Compare_43392
= exact same signal

Audacity Project SpectraREM3LockUnlockCode3333Compare:
REM3Lock1oneTouchCode3333_43392
REMUnlock1Code3333_43392

Audacity Project SpectraREM3REM15Kf1UnlockSameUser1SameCode2345
Compare Unlock signals for same user (1) and code (2345), REM15 and REM3.
REM3UnlockCode2345Compare_43392
REM15Kf1UnlockCode2345Compare_43392

Capture REM15 Kf1 as user 1 signal, code 2345.
REM15Kf1UnlockCode2345Compare_43392

Program user 2, code 1111 as REM15 Kf1
Program user 1, code 2345 as REM3.
Capture REM3 as user 1 signal, code 2345.
REM3UnlockCode2345Compare_43392

= No, the signals are not the same, user and code are the same, but keyfobs serial numbers and signals are not the same.

##RX1 versus RTX3 signal, same user, same code, same keyfob
= Signal sent by Keyfob, is the same, regardless of whether the RX1 or RTX3 module installed.

Note: Only REM15 can work with both RX1 and RTX3
REM15Kf1 is user 2, code 1111

Audacity project - SpectraRX1andRTX3Keyfob1LockCompare

Capture RTX3 Spectra Keyfob 1 Lock signals - compare
RTX3REM15Kf1Lock_43392

Wire up RX1
Capture RX1 Spectra Keyfob 1 Lock signals - compare
RX1REM15Kf1Lock_43392

Comparison = RX1 and RTX3 Same Lock signal sent by keyfob, RTX3 Lock signal is the lesser amplitude signal.

Compare the REM15 Keyfob 1 Lock and Unlock signals as user 1 code 2345, to the REM15 Keyfob 1 Lock and Unlock signals, as user 3 code 2345. 
Capture Keyfob 1 signal as user 1 code2345
RX1Kf1User1Code2345Unlock_43392
RX1Kf1User1Code2345Lock_43392

then program REM15 Kf2 as user 1 code 7890. 
Power+ MC(2345)
user number, 01
7890
7890
press any Keyfob 2 remote button twice (1 second between presses)
clear, clear.

Program REM15 Kf1 as user 3 code 2345, capture Lock and Unlock signal
Power+ MC(7890)
user number, 03
2345
2345
press any Keyfob 1 remote button twice (1 second between presses)
clear, clear.

Capture Keyfob 1 as user 3 code 2345
RX1Kf1User3Code2345Unlock_43392
RX1Kf1User3Code2345Lock_43392

Compare Keyfob 1 Lock and Unlock signals for user 1 and 3, same code.
Audacity Project - SpectraRX1Kf1User1User3Code2345
RX1Kf1User1Lock
RX1Kf1User3Lock
RX1Kf1User1Unlock
RX1Kf1User3Unlock

Lock signals are the same, different user, same code.
Yes, Unlock signals are the same, different user, same code.

###Conclusion: 
Keyfob serial number and/or code are a factor, in the signal Lock or Unlock signal being sent.

Compare pre-captured signals for same Keyfob, same user, but different programmed code.
REM3Lock1oneTouchCode1212_43392
REM3Lock1oneTouchCode1234_43392
REM3Lock1oneTouchCode1111_43392
REM3Lock1oneTouchCode2222_43392
REM3Lock1oneTouchCode3333_43392
REM3Lock1oneTouchCode4444_43392
Four signals in 2 pairs. First pair not same as other signals. Third signal of the 4 are all the same. 

All of the above OneTouch Codes Part 3 of 4 sent back to REM3 are the same signal !!! 
**Different Codes do not have an effect on the signal sent back to REM3.**

REM3Lock1oneTouchCode9999_43392
REM3Unlock1Code9999_43392
REM3Lock1oneTouchCode2222_43392
REM3Unlock1Code2222_43392

Part 1 of 4 (1 of first pair) different.
Part 4 of 4 (4th of second pair) all the same signals.

###Compare RX1 Keyfob 1 Lock and Keyfob 2 Lock, Keyfob 1 Unlock and Keyfob 2 Unlock
RX1Kf1Lock_43392
RX1Kf2Lock_43392
RX1Kf1Unlock_43392
RX1Kf2Unlock_43392

On Windows import as Unsigned 8bit (<- !!), no endianess, Mono, 10000 Hz (decimated)
Spectra kf1 Lock 1
Spectra kf1 Unlock 1
Spectra kf2 Lock 1
Spectra kf2 Unlock 1

**All REM15 Lock signals are the same, if same keyfob, same user, same code.**
**All REM15 Unlock signals are the same, if same keyfob, same user, same code.**
These signals are found on Backup drive (Red WD) in Folder:

###Capture the 4 different buttons on the REM15 Kf1 and compare signals
Capture at 435.72 MHz
Audacity Project - SpectraRX1KF1AllTheButtonsCompared.aup
SpectraRX1KF1ButtonDot1_43572
SpectraRX1KF1ButtonDot2_43572
SpectraRX1KF1ButtonLock_43572 (worked loop 2)
SpectraRX1KF1ButtonUnlock_43572

One symbol 7:00.0000 to 7:00.0391 = 0.0391 seconds. = 25.5754 symbols per second
Double symbol 7:01.6103 to 7:01.6898 = 0.0795 seconds.

###Correct baudrate, symbols per second calcs
Preamble Start and stop and how many symbols, then find out how many symbols per second.
Preamble start 6:59.9590 to stop 7:00.9820. Total preamble =  0.023 seconds = 23 ms
Number of preamble symbols = 13
Symbols per second = 13 / 0.023  = 565.21

###Capture the 4 different buttons on the REM15 Kf2 and compare signals
Capture at 435.72 MHz
Audacity Project - SpectraRX1KF2AllTheButtonsCompared.aup
SpectraRX1KF2ButtonDot1_43572
SpectraRX1KF2ButtonDot2_43572
SpectraRX1KF2ButtonLock_43572
SpectraRX1KF2ButtonUnlock_43572

One symbol  7:00.000 to  7:00.0393 =  0.0393 seconds. 
Double symbol 7:01.4939 to  7:01.5735 =  0.0796 seconds.

###Capture signals off-centre, compare, demodulate and bit convert 
Gnuradio does not come with Sources blocks by default !!! Need gr-osmosdr for that ->

(Install gnuradio-dev
Install libhackrf-dev)

-> Install gr-osmosdr to get osmocom source in gnuradio-companion (install 2 dependencies)

For the HackRF live signal capture, choose osmocom Source block.
Follow Inguardians GRC signal analysis.pdf instructions
Variable Block - freq
Variable Block - samp_rate
Play signal and find out where Peak hold of signal is, DC offset is, channel width, then choose frequency offset based on DC offset and channel width.
Variable Block - channel_spacing

Variable Block - freq_offset = (2000000 + 1000000)/2 + ((2000000 + 1000000)/2) *0.1
Look at Instrumentation - WX - FFT and Waterfall to get info about the DC offset and actual frequencies of the signals.
The bandwidth captured by the HackRF is 9 MHz by default.

Waterfall kept crashing.
FFT shows DC offset moved to 435.72 MHz. Now the transmission at 433.92 can be processed without it's interference.

Choose Channelizer Block - Frequency Xlating FIR Filter
This cuts off the frequency both ends, filters low and High.
Centre frequency -1.8e6
Decided 1.2M transition was alright. Anything below that was overrunning 0 0 0 ....
Used a Gui Widget Block - WX GUI slider for channel_trans to decide best cutoff.

Type Converter Block - Complex to Mag Block, is used for ASK modulated signals.

Filters - Low Pass Filter Block.
GNURadio companion Project: SpectraRX1_DCOffsetRemove_Xlate_Demodulate.grc
Decimation calculation for Low pass filter. Final sample rate cannot be less than the bandwidth left from the low pass filter 
Note: 
fa is the first cutoff frequency. fa needs to be above 0 and less than sampling frequency/2. In this case fa must be above 0 and below 10MHz /2. 
0 < fa <= 5MHz
Choose cutoff frequency of 2MHz
Transition width 1.8 MHz

fb second cutoff frequency, must be 0 < fb  < 5MHz
fa must be more than fb.

Correct symbol rate calc
Synchronizers Block - Clock Recovery MM Block, needs to be a samples per symbol variable.
Samples per second = sample rate = 10000000 Hz
Symbols per second = data rate = you measured this in Spectra signals below.

Measured in Audacity from SDRSharp captured signal.
Capture at 435.72 MHz (freq offset will be = 1.8 MHz in gnuradio)

Spectra keyfob (what were these captured at ? Discovered a strange freq )
Capture again at 435.72 MHz
Preamble = 1.596 seconds high + (01) x 13 + 0.794 (0's) + 2.373 high + 0.7903 (0's)
single symbol = 0.411 seconds
double signal = 0.804 seconds
Whole kf 1 and kf 2 part 1 of 8 signal = 53.953 seconds approx.

Captured at 435.72 MHz
Spectra Reed 1 Open - All 8 parts of the signal are the same as each other.
Spectra Reed 1 Close - All 8 parts of the signal are the same as each other.
Spectra Reed 1 Open and Close first segment, of each of the 8 parts are the same.
Preamble =  3.423 seconds (High, on/off, High, off)
Single symbol =  0.089 seconds
Double symbol =  0.174 seconds

Spectra PIR
Captured at 435.72 MHz
Spectra PIR - All 8 parts of the signal are the same as each other.
Preamble = 3.356 seconds
Single symbol = 0.088 seconds
Double symbol = 0.170 seconds

Process Spectra Reed 1 and PIR - Gnuradio
Process the Spectra Reed 1 and PIR .wav signals in GNURadio, as they have 8 parts and every part is the same

Note the presence of Patterns that are similar between devices and within device signal, means no encryption or data whitening is happening.

Open Audacity and Import - RAW - 32 bit float, Mono, no endianness, 48000
Signal has been "smudged"

Next Low Pass Filter, inspected SpectraDemod  signal, still a wav rather than envelope of signal.

Next  Clock Recover 
Do the symbol per second calculation. 
In ASK baud rate = bit rate
In ASK the baud rate is the same as the bandwidth for an ASK signal.
Single symbol / 0.089 seconds 
X x 0.089 = 1 second = 1/0.089 = 11 symbols / second
Sample rate = 10,000,000 samples / second
10,000,000 / 11 = 909090.909090 samples / symbol

11 bit data rate.  (Symbols per second)

Access Code calculation
Preamble
-  1.596 high / 0.089 symbol /sec = 18 symbols
- (01) x 13  = 26 symbols
- 0.794 (0's) / 0.089 symbol / sec =   9 symbols
- 2.373 high / 0.089 symbol / sec = 26 or 27 symbols
- 0.7903 (0's) / 0.089 symbol / sec = 9 symbols
Because of the uncertainty around the second long high symbol, just use everything up to the first long 0's as the Access Code.
Access Code = 15 1's then 13 01's
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 

Next Binary Slice

Comparing BladeRF to HackRF - Reed 1 capture and replay signal

Standing the keypad up after first 3 Loops seems to have improved the replayability.
HackRF 
hackrf_transfer -a 1 -f 435720000 -r 
Spectra_Reed1_Open_43572_Test
Loop 4
Loop 1
Spectra_Reed1_Close_43572_Test
Loop 1
Loop 1

BladeRF
$ cd bladeRF
Load FPGA
$ bladeRF-cli -l /home/bear/bladeRF/hostedx40-latest.rbf
$ bladeRF-cli -i
(interactive mode)
> set frequency rx 435720000
> set samplerate rx 10M
> set bandwidth rx 8M       (actual 8750000)
> set frequency rx 435720000

>  rx config file=Reed1Open43572 format=bin n=100M
> rx
> rx start
> rx           (to check state)
> rx stop

> tx config file=Reed1Open43572 format=bin repeat=20 delay=1000000
> tx start


##DCT2 Ultra small Door Contact (Reed 2) with RX1
Serial number: 034018

Installation on a Spectra 4000. Works with the RTX3 and detected by RX1.
Open the larger of the 2 door contact units, insert coin cell battery.

Check-in supervision time is set in the control panel.

I nuked the PIR on Zone 4 in the process of enrolling Reed 2 !! But I put the PIR back in, on Zone 5.
Assign the Door Contact to a Zone. Pg 19 Installer manual, Wireless zone assignment.
Wireless, Zone 4, is in programming location 064. Enter the serial number of the Door Contact. 

Pg 19 Magellan SP Spectra Programming Guide
Press Enter, then 0000 (installer code)
064              (wireless Zone 4 programming location)
214097         (Door Contact - Reed 1 serial number)
Clear, clear.

In Zone definition, make Zone 4 Instant.
Enter, 0000 (installer code)
004 (Zone number)
08 (Instant zone type)
1 (Partition)
Enter
Clear, clear.

Tested door contact causes an alarm when triggered, when alarm is set.
Set alarm, 1111 (set alarm code)

Capture door contact open signal using the HackRF, at offset 435720000 (not the 433920000 that it transmits at):
hackrf_transfer -a 1 - f 435720000 -r SpectraDoorContact2_Open1_Unset_43572

Worked first time replay: 
(Loop = SpectraDoorContactOpenLoop)
SpectraDoorContact2_Open1_Set_43392
Loop 1
Loop 1
Loop 1
Loop 1

SpectraDoorContact2_Close1_Set_43392
(Loop = SpectraDoorContactOpenLoop)
Loop 1
Loop 1
Loop 1
Loop 1

SpectraDoorContact2_Close1_Unset_43392
(Loop = SpectraDoorContactCloseLoop)
xLoop 40
Loop 
Loop 
Loop 

SpectraDoorContact2_Open1_Unset_43392
xLoop 40
xLoop 40
Loop 
Loop 
Loop 
Loop 
Loop 
Loop 

Tampered Reed 1 and Reed 2. Tampering did not set off the alarm at all, either Set or Unset. 
Spectra_Reed1 Tamper_435720kHz (captured in SDR#)
Spectra_Reed2 Tamper_435720kHz (captured in SDR#)
Compare Tampered Reed 2 to untampered Reed 2.
Compare Tampered Reed 1 and Tampered Reed 2.

Weird - Tamper Reed 2 is same signal, as Reed 2 Open, but why did alarm not go off with Reed 2 Tamper = because to open Reed I had to separate reed parts, and once separated a retrigger of open zone does not set off alarm !!
Can set Alarm with an open Zone. So will not retrigger if already open and Alarm set.

Open Reed 2 Zone.
Set Alarm.
Tamper did not set Alarm off.
Close Zone then Open again. Yes, retrigger after close, causes an Alarm, but if open already, and you trigger another open, this does not trigger Alarm.

Analysing the Spectra Door Reed 2  signal in gnu radio and calc symbol rate, get binary
Open SDR Signals Linux Binary\Spectra signals\ SpectraDoorContact2_Open1_Set_43392

Import as raw
8 bit signed signal
Mono
10,000000 Hz sample rate

Preamble is many high's, followed by 01 x 13
One symbol is 01

Preamble highs start   
15:40.4655
15:40.2990
----------------
       0.1665 seconds

Symbol 01 
15:40.9594
15:40.8771
-----------------

Symbol 0 or 1

Measured ~4000 samples per symbol in audacity. NOT CORRECT
Calculation based on measurements above = 10,000,000 samp/ sec * 0.04 sec /symbol = 4000 symbols per second = actual data rate.
Decimate 100
Now this kind of gives you a starting point to use, may need to tweak until you get reliable filtered signals ? How to get all 8 parts of a reed signal to be perfectly processed by gnuradio, not just 2 parts of 8 perfect.

Capture spectra reed signal in gnuradio.
Check FFT plot for DC offset and signal strength.

GnuRadio file: SpectraRX1_DCOffsetRemove_Xlate_Demodulate_ClockRec_BinarySlicer.grc
Wrote files:
1Spectra_AddConst_SampSym40, file output after AddConst Block.
2Spectra_AddConst_SampSym40, after Low Pass Filter Block.
3Spectra_AddConst_SampSym40, after Clock Recovery Block.
4Spectra_AddConst_SampSym40, after Binary Slicer Block.

Look at signals in audacity. 2 
32 bit float
Mono
no endianess
10,000,000

Parts 3 and 4 of 8 part 2Spectra_AddConst_SampSym40 are good, but only after first preamble signal, so only 13 x 01 and synch word.

Feed into grc_bit_converter.py, get hex. Figure out bits and shifts that could occur.

