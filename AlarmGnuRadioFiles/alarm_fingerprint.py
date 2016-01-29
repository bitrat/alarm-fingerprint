#!/usr/bin/env python

import re
import string
import logging
import logging.config

auto_logger = logging.getLogger('log_alarm_signals.process_alarm_hex_auto')

def split_bits(s, seps):
    processedbits = [s]
    for sep in seps:
        s, processedbits = processedbits, []
        for seq in s:
            processedbits += seq.split(sep)
    return processedbits

def convert_bits_to_spectra_data(bits_list):
    converted_bit_list = []
    for bitidx, bititem in enumerate(bits_list):
        # match bit counts and convert into the definitive bit
        # minus 2 and minus 1 (split removes bit from one side, or from both sides)
        #7/8/9/10 = one bit either 0 or 1 = 5/6/7/8/9
        #14/15/16/17/18 = two bits either 00 or 11 = 12/13/14/15/16/17
        #32/33/34/35 = preamble 4 x 1 bit = 30/31/32/33/34
        #48/49/50/51/52 = synch word 6 x 1 bit = 46/47/48/49/50/51

        # 4
        if bititem == '0000':
            converted_bit_list.append('0')
        elif bititem == '1111':
            converted_bit_list.append('1')
        # 5
        if bititem == '00000':
            converted_bit_list.append('0')
        elif bititem == '11111':
            converted_bit_list.append('1')
        #6
        elif bititem == '000000':
            converted_bit_list.append('0')
        elif bititem == '111111':
            converted_bit_list.append('1')
        #7
        elif bititem == '0000000':
            converted_bit_list.append('0')
        elif bititem == '1111111':
            converted_bit_list.append('1')
        #8
        elif bititem == '00000000':
            converted_bit_list.append('0')
        elif bititem == '11111111':
            converted_bit_list.append('1')
        #9
        elif bititem == '000000000':
            converted_bit_list.append('0')
        elif bititem == '111111111':
            converted_bit_list.append('1')
        #12
        elif bititem == '000000000000':
            converted_bit_list.append('00')
        elif bititem == '111111111111':
            converted_bit_list.append('11')
        #13
        elif bititem == '0000000000000':
            converted_bit_list.append('00')
        elif bititem == '1111111111111':
            converted_bit_list.append('11')
        #14
        elif bititem == '00000000000000':
            converted_bit_list.append('00')
        elif bititem == '11111111111111':
            converted_bit_list.append('11')
        #15
        elif bititem == '000000000000000':
            converted_bit_list.append('00')
        elif bititem == '111111111111111':
            converted_bit_list.append('11')
        #16
        elif bititem == '0000000000000000':
            converted_bit_list.append('00')
        elif bititem == '1111111111111111':
            converted_bit_list.append('11')
        #17
        elif bititem == '00000000000000000':
            converted_bit_list.append('00')
        elif bititem == '11111111111111111':
            converted_bit_list.append('11')
        #30
        elif bititem == '111111111111111111111111111111':
            converted_bit_list.append('1111')
        #31
        elif bititem == '1111111111111111111111111111111':
            converted_bit_list.append('1111')
        #32
        elif bititem == '11111111111111111111111111111111':
            converted_bit_list.append('1111')
        #33
        elif bititem == '111111111111111111111111111111111':
            converted_bit_list.append('1111')
        #34
        elif bititem == '1111111111111111111111111111111111':
            converted_bit_list.append('1111')
        #46
        elif bititem == '1111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
        #47
        elif bititem == '11111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
        #48
        elif bititem == '111111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
        #49
        elif bititem == '1111111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
        #50
        elif bititem == '11111111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
        #51
        elif bititem == '111111111111111111111111111111111111111111111111111':
            converted_bit_list.append('111111')
#        else:
#            converted_bit_list.append('xxxxxx')

    return converted_bit_list

def convert_bits_to_yale_data(bits_list):
    converted_bit_list = []
    for bitidx, bititem in enumerate(bits_list):
        # match the statistically determined hex 0 and f counts, and convert them into the 0 and 1 symbol bits
        # '' (the original split removes 0 bits from 2 sides, replace with a 0)
        # 0's = '' to 4 = 0 
        # 0's = 5 to 10 = 00
        # 1's = 1 to 6 = 1
        # 1's = 7 to 11 = 11

        # ''
        if bititem == '':
            converted_bit_list.append('0')
        # 1
        if bititem == '0':
            converted_bit_list.append('0')
        elif bititem == 'f':
            converted_bit_list.append('1')
        # 2
        if bititem == '00':
            converted_bit_list.append('0')
        elif bititem == 'ff':
            converted_bit_list.append('1')
        # 3
        if bititem == '000':
            converted_bit_list.append('0')
        elif bititem == 'fff':
            converted_bit_list.append('1')
        # 4
        if bititem == '0000':
            converted_bit_list.append('0')
        elif bititem == 'ffff':
            converted_bit_list.append('1')
        # 5
        if bititem == '00000':
            converted_bit_list.append('00')
        elif bititem == 'fffff':
            converted_bit_list.append('1')
        #6
        elif bititem == '000000':
            converted_bit_list.append('00')
        elif bititem == 'ffffff':
            converted_bit_list.append('1')
        #7
        elif bititem == '0000000':
            converted_bit_list.append('00')
        elif bititem == 'fffffff':
            converted_bit_list.append('11')
        #8
        elif bititem == '00000000':
            converted_bit_list.append('00')
        elif bititem == 'ffffffff':
            converted_bit_list.append('11')
        #9
        elif bititem == '000000000':
            converted_bit_list.append('00')
        elif bititem == 'fffffffff':
            converted_bit_list.append('11')
        #10
        elif bititem == '0000000000':
            converted_bit_list.append('00')
        elif bititem == 'ffffffffff':
            converted_bit_list.append('11')
        #11
        elif bititem == '00000000000':
            converted_bit_list.append('00')
        elif bititem == 'fffffffffff':
            converted_bit_list.append('11')
        #12
        elif bititem == '000000000000':
            converted_bit_list.append('00')
        elif bititem == 'ffffffffffff':
            converted_bit_list.append('11')

        #36
        elif bititem == 'ffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #37
        elif bititem == 'fffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #38
        elif bititem == 'ffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #39
        elif bititem == 'fffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #40
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #41
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #42
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #43
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #44
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #45
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #46
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #47
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #48
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #49
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #50
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #51
        elif bititem == 'fffffffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')
        #52
        elif bititem == 'ffffffffffffffffffffffffffffffffffffffffffffffffffff':
            converted_bit_list.append('111111')

    return converted_bit_list

def convert_bits_to_bosch_data(bits_list):
    converted_bit_list = []
    for bitidx, bititem in enumerate(bits_list):
        # match the statistically determined hex 0 and f counts, and convert them into the 0 and 1 symbol bits

        #10
        if bititem == '0000000000':
            converted_bit_list.append('0')
        elif bititem == 'ffffffffff':
            converted_bit_list.append('1')
        #11
        elif bititem == '00000000000':
            converted_bit_list.append('0')
        elif bititem == 'fffffffffff':
            converted_bit_list.append('1')
        #12
        elif bititem == '000000000000':
            converted_bit_list.append('0')
        elif bititem == 'ffffffffffff':
            converted_bit_list.append('1')
        #13
        elif bititem == '0000000000000':
            converted_bit_list.append('0')
        elif bititem == 'fffffffffffff':
            converted_bit_list.append('1')

        #22
        elif bititem == 'ffffffffffffffffffffff':
            converted_bit_list.append('11')
        elif bititem == '0000000000000000000000':
            converted_bit_list.append('00')
        #23
        elif bititem == 'fffffffffffffffffffffff':
            converted_bit_list.append('11')
        elif bititem == '00000000000000000000000':
            converted_bit_list.append('00')
        #24
        elif bititem == 'ffffffffffffffffffffffff':
            converted_bit_list.append('11')   
        elif bititem == '000000000000000000000000':
            converted_bit_list.append('00')
        #25
        elif bititem == 'fffffffffffffffffffffffff':
            converted_bit_list.append('11') 
        elif bititem == '0000000000000000000000000':
            converted_bit_list.append('00')
        #26
        elif bititem == 'ffffffffffffffffffffffffff':
            converted_bit_list.append('11')
        elif bititem == '00000000000000000000000000':
            converted_bit_list.append('00')

    return converted_bit_list

def extract_packet(matchPreamble, extractPacketStart, alarmIdentified, indata, count):
    output_file = []

    if alarmIdentified == "DSCAlexxor":
        # extract Packet, precise Packet End for a DSC signal is not needed ( multiple 00's at end of each packet)
        extractPacketEnd = extractPacketStart + 72
        extractedPacket = indata[extractPacketStart:extractPacketEnd]
        if extractedPacket:
            auto_logger.debug("%s Complete Signal Packet:\n%s\n", alarmIdentified,extractedPacket)

            if matchPreamble == '\\x00\\x00\\x00\\x03\\xff\\x55' or matchPreamble == '\\x00\\x00\\x00\\x0f\\xfd\\x55' or matchPreamble == '\\x00\\x00\\x00\\x01\\xfd\\x55' or matchPreamble == '\\x00\\x00\\x00\\x07\\xfe\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x01\\xff\\xaa': 
                # Offset = Extract Hex : Preamble + Synch Word + 01 status bit
                offset = 24
                extractedPacketData = extract_data(extractedPacket,offset)
            elif matchPreamble == '\\x00\\x00\\x00\\x7f\\x55' or matchPreamble == '\\x00\\x00\\x00\\x3f\\x55' or matchPreamble == '\\x00\\x00\\x00\\x3f\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x1f\\xaa' or matchPreamble == '\\x00\\x00\\x00\\xfd\\x55' or matchPreamble == '\\x00\\x00\\x00\\xfe\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x7e\\xaa':
                offset = 20
                extractedPacketData = extract_data(extractedPacket,offset)
            elif matchPreamble == '\\x00\\x00\\x00\\x3f\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x03\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x7f\\xf5' or matchPreamble == '\\x00\\x00\\x00\\xff\\xd5' or matchPreamble == '\\x00\\x00\\x00\\x1f\\xd5' or matchPreamble == '\\x00\\x00\\x00\\x03\\xfa\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x7f\\xea' or matchPreamble == '\\x00\\x00\\x00\\x1f\\xfa\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x0f\\xea' or matchPreamble == '\\x00\\x00\\x00\\x07\\xea' or matchPreamble == '\\x00\\x00\\x00\\x01\\xfa\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x07\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x0f\\xd5':
                offset = 23
                extractedPacketData = extract_data(extractedPacket,offset)

            # If no currently recognised Alarm signals detected
            else:
                 extractedPacketData = ""

            if extractedPacketData:
            #Extract and process binary from hex
                hexPacketData = string.replace(extractedPacketData,"\\x","")

             # If there is multiple zero data hex (3 x00), signal is chopped
             # Discard from further processing
                if hexPacketData[13:24] == "00000000000":
                    auto_logger.debug("DISCARD Signal: MALFORMED")
                    auto_logger.debug("--------------------------------")
                    output_file.append("")
                    count +=0
                else: 
                    auto_logger.debug("Extracted Hex: %s",hexPacketData) 
                    auto_logger.debug("--                           ---")
                    output_hexPacketData = "Extracted Hex: \n"+"                              "+hexPacketData+"\n                              -----------------------------------------------------------\n"

                    extractedBinary = hex_to_binary(hexPacketData)
                    auto_logger.debug("Extracted Binary:\n%s",extractedBinary)

                    # Process the Data into the Device Module type and Status
                    deviceData = remove_non_data(matchPreamble,extractedBinary)
                    try:
                        chksignal, status = device_status(deviceData, alarmIdentified, hexPacketData)
                    except (TypeError, ValueError):
                        #auto_logger.debug("No Status information found in signal. Continue to next .dat file")
                        status = ""
                    if status:
                         output_file.append(output_hexPacketData)
                         output_file.append(status[0])
                         count +=1
                         serial_num = check_device_type(deviceData, alarmIdentified)
                         if serial_num:
                             for serialnum_item in serial_num:
                                 output_file.append(serialnum_item)                       
                    else:
                         output_file.append("")  
                         count +=0   
                      
                # Depending on whether signal contains any recognizable signals, count > 0, keep original file
                return count, output_file

    elif alarmIdentified == "Spectra4000":
        # extract Packet, use a max Packet size 
        # TO DO: Add REM3 Keyfob code. It has a much longer signal than the DCT2 Reeds, REM15 Keyfobs and PIRs
        extractPacketEnd = extractPacketStart + 640
        extractedPacket = indata[extractPacketStart:extractPacketEnd]
        if extractedPacket:
            #auto_logger.debug("%s Complete Signal Packet:\n%s\n", alarmIdentified, extractedPacket)
            extractedPacketData = extract_data(extractedPacket,0)

            if extractedPacketData:            
                hexPacketData = string.replace(extractedPacketData,"\\x","")
                auto_logger.debug("Extracted Hex: %s",hexPacketData) 
                auto_logger.debug("--                           ---")
                extractedBinary = hex_to_binary(hexPacketData)
                #auto_logger.debug("Extracted Binary:\n%s",extractedBinary)

                # Error correction
                errCorrBinary = extractedBinary.replace("010", "000")
                #auto_logger.debug("Error Corrected Binary 010 = 000:\n%s",errCorrBinary)

                try:
                    chksignal, status = device_status(errCorrBinary, alarmIdentified, hexPacketData)
                except (TypeError, ValueError):
                    #auto_logger.debug("No Status information found in signal. Continue to next .dat file")
                    status = ""

                if status:
                    output_file.append(status[0])
                    count +=1
                else:
                    output_file.append("")
                    count +=0

        return count, output_file

    elif alarmIdentified == "YaleStandard":

        if indata:
            hexPacketData = indata.replace("\\x", "")
            errCorrBinary = "000"

            try:
                chksignal, status = device_status(errCorrBinary, alarmIdentified, hexPacketData)
            except (TypeError, ValueError):
                #auto_logger.debug("No Status information found in signal. Continue to next .dat file")
                status = ""

            if status:
                auto_logger.debug("Check Signal: %s", chksignal)              
                auto_logger.debug("Status: %s", status)
                output_file.append(status[0])
                count +=1
            else:
                output_file.append("")

        return count, output_file

    elif alarmIdentified == "Bosch3000":

        if indata:
            hexPacketData = indata.replace("\\x", "")
            errCorrBinary = "000"
            try:
                chksignal, status = device_status(errCorrBinary, alarmIdentified, hexPacketData)
            except (TypeError, ValueError):
                #auto_logger.debug("No Status information found in signal. Continue to next .dat file")
                status = ""

            if status:
                output_file.append(status[0])
                state = check_device_type(hexPacketData, alarmIdentified)

                if state:
                    for state_item in state:
                        output_file.append(state_item)
                count +=1
            else:
                output_file.append("")
                count +=0

        return count, output_file
    else:
        auto_logger.debug("No Alarm identified, no Packets extracted.")
        count +=0
        output_file.append("")
        auto_logger.debug(output_file)
        return count, output_file

def extract_data(extractedPacket,extractDataStart):
    extractedPacketData = extractedPacket[extractDataStart:]  
    #auto_logger.debug("Extracted Packet Data:\n%s\n",extractedPacketData)
    return extractedPacketData

def extract_bosch_packet(hexPacketData):

    bosch_bits_list = split_bits(hexPacketData, ['1', '3','7', '8','c', 'e','0f', 'f0'])
    bosch_data_list = convert_bits_to_bosch_data(bosch_bits_list)

    # Check for presence of Bosch peripheral Preamble, then what the peripheral is, what status, or check if the signal is a keyfob key press status       
    bosch_data_parts_list = []
    bosch_data_parts_list = ''.join(bosch_data_list)

    # Split according to the consistent Preamble 11001100110011001100110010101011
    bosch_signal_list = split_bits(bosch_data_parts_list, ['11001100110011001100110010101011'])
    return bosch_signal_list

def remove_non_data(matchPreamble,extractedBinary):  
    if matchPreamble == '\\x00\\x00\\x00\\x03\\xff\\x55' or matchPreamble == '\\x00\\x00\\x00\\x3f\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x07\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x03\\xf5' or matchPreamble == '\\x00\\x00\\x00\\x3f\\x55' or matchPreamble == '\\x00\\x00\\x00\\x7f\\x55' or matchPreamble == '\\x00\\x00\\x00\\x3f\\x55':
     # Remove first 01
     # Rest is Device Data
        extractBinary = extractedBinary[2:]
     # Convert to single bit Binary
        dataBinary = convert_2bit(extractBinary)
    elif matchPreamble == '\\x00\\x00\\x00\\x3f\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x03\\xfa\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x1f\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x1f\\xfa\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x01\\xff\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x01\\xfa\\xaa': 
     # Remove 101
     # Rest is Device Data
        extractBinary = extractedBinary[3:]
     # Convert to single bit Binary
        dataBinary = convert_2bit(extractBinary)
    elif matchPreamble == '\\x00\\x00\\x00\\x7f\\xea' or matchPreamble == '\\x00\\x00\\x00\\x07\\xfe\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x0f\\xea' or matchPreamble == '\\x00\\x00\\x00\\x07\\xea' or matchPreamble == '\\x00\\x00\\x00\\xfe\\xaa' or matchPreamble == '\\x00\\x00\\x00\\x7e\\xaa':
     # Remove 1
     # Rest is Device Data
        extractBinary = extractedBinary[1:]
     # Convert to single bit Binary
        dataBinary = convert_2bit(extractBinary)
    else:
        dataBinary = convert_2bit(extractedBinary)
        auto_logger.debug("No Binary removed")

    auto_logger.debug("Converted binary:\n%s",dataBinary)
    return dataBinary

def device_status(deviceData, alarmIdentified, hexPacketData):

    status_output = []

    if alarmIdentified == "DSCAlexxor":
        # Status = 8 bits
        statusDevice = deviceData[0:8]
        if statusDevice == '01000011':
            status_console = "Status of Device:     Open\n-----------------------------------------------------------\n"
            status = "Status of Device:     Open\n                              -----------------------------------------------------------\n"
            auto_logger.info(status_console)
            status_output.append(status)
            return status, status_output
        elif statusDevice == '01000111':
            status_console = "Status of Device:     Close\n-----------------------------------------------------------\n"
            status = "Status of Device:     Close\n                              -----------------------------------------------------------\n"
            auto_logger.info(status_console)
            status_output.append(status)
            return status, status_output
        elif statusDevice == '00000101':
            status_console = "Status of Device:     Unlock button pressed\n-----------------------------------------------------------\n"
            status = "Status of Device:     Unlock button pressed\n                              -----------------------------------------------------------\n"
            auto_logger.info(status_console)
            status_output.append(status)
            return status, status_output
        elif statusDevice == '00001111':
            status_console = "Status of Device:     Lock Key was pressed\n-----------------------------------------------------------\n"
            status = "Status of Device:     Lock Key was pressed\n                              -----------------------------------------------------------\n"
            auto_logger.info(status_console)
            status_output.append(status)
            return status, status_output
        elif statusDevice == '00000011':
            status_console = "Status of Device:     Stay Arm Key was pressed\n-----------------------------------------------------------\n"
            status = "Status of Device:     Stay Arm Key was pressed\n                              -----------------------------------------------------------\n"
            auto_logger.info(status_console)
            status_output.append(status)
            return status, status_output

    elif alarmIdentified == "Spectra4000":

        # Process the Data into the Device Module type and Status
        spectra_bits_list = split_bits(deviceData, ['01', '10'])
        spectra_bit_len = len(spectra_bits_list)
        processed_spectra_bit_list = convert_bits_to_spectra_data(spectra_bits_list)
        processed_spectra_bit_len = len(processed_spectra_bit_list)

        if processed_spectra_bit_list:
            spectra_signal_start = 0
            for index, elem in enumerate(processed_spectra_bit_list):
                # Last High (1) signal will have all it's 0's chopped off, replace those
                if processed_spectra_bit_list[processed_spectra_bit_len-1] == '1':
                    processed_spectra_bit_list[processed_spectra_bit_len-1] = 100
                elif processed_spectra_bit_list[processed_spectra_bit_len-1] == '11':
                    processed_spectra_bit_list[processed_spectra_bit_len-1] = 110
                if processed_spectra_bit_list[index] == '111111':
                    spectra_signal_start = index

           # Access, and join the bits that indicate Keyfob, Reed and PIR status
           # bits 17 - 24 (Unlock data bits 21 - 24 )
            spectra_status_start = spectra_signal_start+34
            spectra_status_end = spectra_status_start+16
            spectra_status = [''.join(str(v) for v in processed_spectra_bit_list[spectra_status_start:spectra_status_end])]
                
            # Keyfob Unlock signal last 4 bits, bit 21 to 14 used as identifier
            spectra_status_last4bits = spectra_status[0][12:]

            if spectra_status[0] == '110110110110100110110110':
                status_console = "-----------------------------------------------------------\nSpectra Reed Open Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra Reed Open Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '110110110110100110110110':
                status_console = "-----------------------------------------------------------\nSpectra Reed Close Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra Reed Close Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '100110110110110100110110':
                status_console = "-----------------------------------------------------------\nSpectra PIR Open Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra PIR Open Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '110110110110110110100110':
                status_console = "-----------------------------------------------------------\nSpectra REM15 Keyfob Lock Button Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra REM15 Keyfob Lock Button Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '100110110110110110100110':
                status_console = "-----------------------------------------------------------\nSpectra REM15 Keyfob Dot1 Lock Button Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra REM15 Keyfob Dot1 Lock Button Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '110100110110110110100110':
                status_console = "-----------------------------------------------------------\nSpectra REM15 Keyfob Dot2 Button Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra REM15 Keyfob Dot2 Button Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output
            elif spectra_status[0] == '100100100110110100100100':
                status_console = "-----------------------------------------------------------\nSpectra REM3 Keyfob Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra REM3 Keyfob Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status[0], status_output


            # Unlock - bits 21 to 24 in common 
            elif spectra_status_last4bits == '100110100110':
                status_console = "-----------------------------------------------------------\nSpectra REM15 Keyfob Unlock Button Signal Detected.\n-----------------------------------------------------------"
                status = "-----------------------------------------------------------\n------------------------------ Spectra REM15 Keyfob Unlock Button Signal Detected.\n-----------------------------------------------------------------------------------------"
                auto_logger.info(status_console)
                status_output.append(status)
                return spectra_status_last4bits, status_output

    elif alarmIdentified == "YaleStandard":
        yale_bits_list = split_bits(hexPacketData, ['1', '3','7', '8','c', 'e', '\n', '0f', 'f0'])
        yale_bit_len = len(yale_bits_list)
        yale_data_list = convert_bits_to_yale_data(yale_bits_list)
        if yale_data_list:

            yale_preamble_idx = [i for i, item in enumerate(yale_data_list) if re.search('111111', item)]

            # what peripheral, or keyfob key press status
            # Yale data is 6 signal blocks of data
            # Yale Lock and Unlock signal are 2 unique signal blocks - check for these first
            # Yale Lock identifier -   1111110110010110010110110110110110110110110110011111101100101100100101101101100101101101101100
            # Yale Unlock identifier - 1111110110010110010110110110110110110110010010011111101100101100100101101101101100100101100100
   
            # Yale peripheral string will be 1111110110010110010110110110110110110110110010
            # Check past 3 signal blocks forwards from the Yale peripheral string +4 to +5, to determine device type, or, 
            # if nothing detected (because signal too degraded) check backwards, blocks -2 to -1 from the Yale peripheral string
            # Yale Reed string - 11111101100101100101100101100100101101101100101111110110010110010110110110110010110110110110
            # Yale PIR string -  11111101100101100101101101101101101100100100101111110110010110010110110110010010110110110110
            # = Yale parts (6 parts make up a  complete signal)
            yale_data_parts_list = []
            for index, elem in enumerate(yale_preamble_idx):
                curr_index = yale_preamble_idx[index]
                list_len = len(yale_preamble_idx)
                if index < len(yale_preamble_idx)-3:
                    next_index_part1 = yale_preamble_idx[index+1]
                    next_index_part2 = yale_preamble_idx[index+2]
                    next_index_part3 = yale_preamble_idx[index+3]
                    if next_index_part1 != curr_index:
                        yale_data_part = ''.join(yale_data_list[curr_index:next_index_part1])
                        if next_index_part2 != next_index_part1:
                            yale_data_part_next = ''.join(yale_data_list[next_index_part1:next_index_part2])
                            yale_data_part_afternext = ''.join(yale_data_list[next_index_part2:next_index_part3])
 
                            # "break" simply logs first instance of a yale signal in the Capture .cap file
                            # remove "break" if you want to detect all the multiple instances of signals 

                            if (yale_data_part == '11111101100101100101101101101101101101101101100'):
                                if (yale_data_part_next == '11111101100101100100101101101100101101101101100'):
                                    status_console = "Yale Standard Lock Signal identified.   \n-----------------------------------------------------------"
                                    status = "Yale Standard Lock Signal identified.\n                          -----------------------------------------------------------"
                                    auto_logger.info(status_console)
                                    status_output.append(status)
                                    return yale_data_part, status_output
                                    break

                            elif (yale_data_part == '11111101100101100101101101101101101101100100100'):
                                if (yale_data_part_next == '11111101100101100100101101101101100100101100100'):
                                    status_console = "Yale Standard Unlock Signal identified.   \n-----------------------------------------------------------"
                                    status = "Yale Standard Unlock Signal identified.\n                          -----------------------------------------------------------"
                                    auto_logger.info(status_console)
                                    status_output.append(status)
                                    return yale_data_part, status_output
                                    break

                            elif (yale_data_part_afternext == '1111110110010110010110110110110110110110110010'):
                                print "\nYale Standard Peripheral identified :"
                                if (yale_data_part == '1111110110010110010110110110110110110010010010'):
                                    if (yale_data_part_next == '1111110110010110010110110110010010110110110110'):
                                        status_console = " Yale Standard PIR signal.   \n-----------------------------------------------------------"
                                        status = "Yale Standard Peripheral identified : Yale PIR signal\n                          -----------------------------------------------------------"
                                        auto_logger.info(status_console)
                                        status_output.append(status)
                                        return yale_data_part, status_output
                                        break

                                elif (yale_data_part == '1111110110010110010110010110010010110110110010'):
                                    if (yale_data_part_next == '1111110110010110010110110110110010110110110110'):
                                        status_console = " Yale Standard Reed signal.   \n-----------------------------------------------------------"
                                        status = "Yale Standard Peripheral identified : Yale Reed signal\n                          -----------------------------------------------------------"
                                        auto_logger.info(status_console)
                                        status_output.append(status)
                                        return yale_data_part, status_output
                                        break  

    elif alarmIdentified == "Bosch3000":

        bosch_signal_list = extract_bosch_packet(hexPacketData)

        if bosch_signal_list:
            for index, elem in enumerate(bosch_signal_list):
                if index <= len(bosch_signal_list):
                    if bosch_signal_list[index]:

                        # Extract Peripheral status information - index 64:80 = Status info
                        bosch_signal_status = bosch_signal_list[index][64:80]

                        if bosch_signal_status == '0011010101010100':
                            status_console = "Device Status:       Open\n"
                            status = "Device Status:       Open\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output
                        elif bosch_signal_status == '0101010101010100':
                            status_console = "Device Status:       Close\n"
                            status = "Device Status:       Close\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output
                        elif bosch_signal_status == '0101001101010100':
                            status_console = "Device Status:       Lock Button\n"
                            status = "Device Status:       Lock Button\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output
                        elif bosch_signal_status == '0100110101010100':
                            status_console = "Device Status:       Unlock Button\n"
                            status = "Device Status:       Unlock Button\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output
                        elif bosch_signal_status == '0101010011010100':
                            status_console = "Device Status:       Dot 1 Button\n"
                            status = "Device Status:       Dot 1 Button\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output
                        elif bosch_signal_status == '0101010100110100':
                            status_console = "Device Status:       Dot 2 Button\n"
                            status = "Device Status:       Dot 2 Button\n"
                            auto_logger.info(status_console)
                            status_output.append(status)
                            return status, status_output

def hex_to_binary(hexPacketData):
        scale = 16
        num_of_bits = 4

        # Insert a temp '1', otherwise leading binary zeros lost
        try:
            extractedBinary = bin(int('1'+hexPacketData,scale))[3:].zfill(num_of_bits)
            return extractedBinary
        except Exception as error:
            auto_logger.debug("Could not convert hex value in %s, into alarm ID data.",from_file, exc_info=True)

def convert_2bit(signalBinary):
    # 2 bits (01,00) LSB represents actual signal bit
    return signalBinary[1::2]

def check_device_type(deviceData, alarmIdentified):

    output_devicetype = []

    if (alarmIdentified == "DSCAlexxor"):
#      for loop extracts Serial Numbers of Format:
#      SN1 SN2 1 SN3 SN4 1 SN5 SN6
        serialNumberParts = []
        completeSN = []
        start=8
        end=start+4
        for i in range(0,6):
            n = deviceData[start:end]         
            serialNumberParts.append(n)
            try:
                completeSerialNumber = hex(int(n,2))[2:]
            except:
                auto_logger.debug("No valid hex value to construct serial number")

            if (i==1 or i==3):
                start = start+1
                end = start+1
            start = start+4
            end = start+4
            completeSN.append(completeSerialNumber)
        totalSN = ''.join(completeSN)

      # Check DSC Module number to determine Device type    
        if (deviceData[8:12] == "0010"):
            deviceTypeHex = hex(int(deviceData[8:12],2))[2:]
            auto_logger.info("Device Serial Number: %s",totalSN)
            auto_logger.info("Device Module:        %s",deviceTypeHex)
            deviceType = "DSC Reed"
            auto_logger.info("Device Type:          %s",deviceType)
            auto_logger.info("--------------------------------")
            auto_logger.info("--------------------------------")
            output_devicetype.append("Device Serial Number: "+totalSN+"\n")
            output_devicetype.append("Device Module:       "+deviceTypeHex+"\n")
            output_devicetype.append("Device Type:         "+deviceType+"\n") 
            output_devicetype.append("-----------------------------------------------------------\n")
            output_devicetype.append("-----------------------------------------------------------\n")
            return output_devicetype

        elif (deviceData[8:12] == "0011"):
            deviceTypeHex = hex(int(deviceData[8:12],2))[2:]
            auto_logger.info("Device Serial Number: %s",totalSN)
            auto_logger.info("Device Module:        %s",deviceTypeHex)
            deviceType = "DSC PIR"
            auto_logger.info("Device Type:          %s",deviceType)
            auto_logger.info("--------------------------------")
            auto_logger.info("--------------------------------")
            output_devicetype.append("Device Serial Number: "+totalSN+"\n")
            output_devicetype.append("Device Module:       "+deviceTypeHex+"\n")
            output_devicetype.append("Device Type:         "+deviceType+"\n") 
            output_devicetype.append("-----------------------------------------------------------\n")
            output_devicetype.append("-----------------------------------------------------------\n")
            return output_devicetype

        elif (deviceData[8:12] == "0110"):
            deviceTypeHex = hex(int(deviceData[8:12],2))[2:]
            auto_logger.info("Device Serial Number: %s",totalSN)
            auto_logger.info("Device Module:        %s",deviceTypeHex)
            deviceType = "DSC WS4939 Keyfob"
            auto_logger.info("Device Type:          %s",deviceType)
            auto_logger.info("--------------------------------")
            auto_logger.info("--------------------------------")
            output_devicetype.append("Device Serial Number: "+totalSN+"\n")
            output_devicetype.append("Device Module:       "+deviceTypeHex+"\n")
            output_devicetype.append("Device Type:         "+deviceType+"\n") 
            output_devicetype.append("-----------------------------------------------------------\n")
            output_devicetype.append("-----------------------------------------------------------\n")
            return output_devicetype

        else:
            output_devicetype.append("")
            return output_devicetype  

    elif (alarmIdentified == "Bosch3000"): 

        bosch_signal_list = extract_bosch_packet(deviceData)

        if bosch_signal_list:
            for index, elem in enumerate(bosch_signal_list):

                if index <= len(bosch_signal_list):

                    if bosch_signal_list[index]:
                        # Extract Peripheral category information - index 33:64 = Peripheral info
                        bosch_signal_peripheral = bosch_signal_list[index][33:64]

                        if bosch_signal_peripheral == '0101011010101001100110011010101':
                            deviceType = "Bosch PIR"
                            auto_logger.info("Device Type:          %s",deviceType)
                            auto_logger.info("--------------------------------")
                            output_devicetype.append("Device Type:         "+deviceType+"\n") 
                            output_devicetype.append("-----------------------------------------------------------\n")
                            output_devicetype.append("-----------------------------------------------------------\n")
                            return output_devicetype

                        elif bosch_signal_peripheral == '0110011001010110101010010110101':
                            deviceType = "Bosch Reed"
                            auto_logger.info("Device Type:          %s",deviceType)
                            auto_logger.info("--------------------------------")
                            output_devicetype.append("Device Type:         "+deviceType+"\n") 
                            output_devicetype.append("-----------------------------------------------------------\n")
                            output_devicetype.append("-----------------------------------------------------------\n")
                            return output_devicetype

                        elif bosch_signal_peripheral == '0110011001010110100101011010101':
                            deviceType = "Bosch Keyfob"
                            auto_logger.info("Device Type:          %s",deviceType)
                            auto_logger.info("--------------------------------")
                            output_devicetype.append("Device Type:         "+deviceType+"\n") 
                            output_devicetype.append("-----------------------------------------------------------\n")
                            output_devicetype.append("-----------------------------------------------------------\n")
                            return output_devicetype
                        else:
                            output_devicetype.append("")
                            return output_devicetype

