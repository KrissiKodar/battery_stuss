import serial
from serial.tools import list_ports
from serial import Serial
import sys
import time
port = list(list_ports.comports())
print(port)
for p in port:
    print(p.device)

BAUD = 250000
# serial port is at /dev/ttyUSB0
ser = Serial('/dev/ttyUSB0', BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    

class battery_gauge:
    def __init__(self):
        # wait for Arduino to be ready
        self.wait_and_print()
    
    def bytes_to_hex(self, data):
        return " ".join([hex(b)[2:].zfill(2) for b in data])

    # same as bytes to hex but put them in a list
    def bytes_to_hex_list(self, data):
        return [hex(b)[2:].zfill(2) for b in data]

    # function that only waits and prints out recieved bytes
    # it should wait until at least 1 byte is available
    def wait_and_print(self):
        print()
        while True:
            if ser.in_waiting > 0:
                print(f'read {ser.in_waiting} bytes')
                data = ser.read(ser.in_waiting)
                print(self.bytes_to_hex_list(data))
                break
        print()

    def wait_and_get_data(self):
        while True:
            if ser.in_waiting > 0:
                #print(f'read {ser.in_waiting} bytes')
                data = ser.read(ser.in_waiting)
                #print(bytes_to_hex(data))
                # put data in 2 nd index of list of dict
                data_read = self.bytes_to_hex_list(data)
                #remove first 5 bytes from the list and also the last byte
                data_read = data_read[6:-1]
                break
        return data_read

    def send_command(self, command):
        # take sum everything except the first byte and add it to the end of the command
        command.append(sum(command[1:]) % 256)
        #print("sending command: ", bytes_to_hex(command))
        ser.write(command)
        #wait_and_print()
        return self.wait_and_get_data()

    def write_word(self, address, data):
        # write 2 bytes to the given address
        write_word = [0x3D, 0x00, 0x05, 0x05, 0x02, address, data[1], data[0]]
        return self.send_command(write_word)
    
    def write_block(self, address, data):
        write_block = [0x3D, 0x00, 0x05, 0x05, 0x03, address, data[1], data[0]] # ath svissast
        return self.send_command(write_block)

    
    def read_word(self, address):
        # read 2 bytes from the given address
        read_word = [0x3D, 0x00, 0x03, 0x04, 0x02, address]
        return self.send_command(read_word)

    def read_block(self, address):
        read_block = [0x3D, 0x00, 0x03, 0x04, 0x03, address]
        return self.send_command(read_block)

    def read_SBS_from_battery(self, registers):
        for key, value in registers.items():
            if value[0] == 'word':
                value[2] = self.read_word(value[1])
            elif value[0] == 'block':
                value[2] = self.read_block(value[1])
            time.sleep(0.05)
        self.order_bytes(registers)
    
    def order_bytes(self, registers):
        for key, value in registers.items():
            if value[0] == 'block':
                if value[-1] == 'flags':
                    # if list not empty
                    if value[2]:
                        if value[2][0] == '03':
                            # remove first index of list
                            value[2].pop(0)
                            # reverse the last 2 indexes of the list
                            value[2][-2:] = value[2][-1], value[2][-2]
                        elif value[2][0] == '04': 
                            # remove first index of list
                            value[2].pop(0)
                            # revere the last 2 indexes of the list
                            value[2][-2:] = value[2][-1], value[2][-2]
                            # reverse the first 2 indexes of the list
                            value[2][:2] = value[2][1], value[2][0]




class BQ4050(battery_gauge):
# init function
    def __init__(self):
        super().__init__()
        self.reg_dict = { 'RemainingCapacityAlarm': ['word', 0x01, None, 'uint16', 'mAh'],
                    'RemainingTimeAlarm':     ['word', 0x02, None, 'uint16', 'min'],
                    'BatteryMode':            ['word', 0x03, None, 'uint16', 'flags'],
                    'AtRate':                 ['word', 0x04, None, 'int16', 'mA'],
                    'AtRateTimeToFull':       ['word', 0x05, None, 'uint16', 'min'],
                    'AtRateTimeToEmpty':      ['word', 0x06, None, 'uint16', 'min'],
                    'AtRateOK':               ['word', 0x07, None, 'uint8', ''],
                    'Temperature':            ['word', 0x08, None, 'int16', '0.1*K'],
                    'Voltage':                ['word', 0x09, None, 'uint16', 'mV'],
                    'Current':                ['word', 0x0A, None, 'int16', 'mA'],
                    'AverageCurrent':         ['word', 0x0B, None, 'int16', 'mA'],
                    'MaxError':               ['word', 0x0C, None, 'uint8', 'mA'],
                    'RelativeStateOfCharge':  ['word', 0x0D, None, 'uint8', '%'],
                    'AbsoluteStateOfCharge':  ['word', 0x0E, None, 'uint8', '%'],
                    'RemainingCapacity':      ['word', 0x0F, None, 'uint16', 'mAh'],
                    'FullChargeCapacity':     ['word', 0x10, None, 'uint16', 'mAh'],
                    'RunTimeToEmpty':         ['word', 0x11, None, 'uint16', 'min'],
                    'AverageTimeToEmpty':     ['word', 0x12, None, 'uint16', 'min'],
                    'AverageTimeToFull':      ['word', 0x13, None, 'uint16', 'min'],
                    'ChargingCurrent':        ['word', 0x14, None, 'uint16', 'mA'],
                    'ChargingVoltage':        ['word', 0x15, None, 'uint16', 'mV'],
                    'BatteryStatus':          ['word', 0x16, None, 'uint16', 'flags'],
                    'CycleCount':             ['word', 0x17, None, 'uint16', ''],
                    'DesignCapacity':         ['word', 0x18, None, 'uint16', 'mAh'],
                    'DesignVoltage':          ['word', 0x19, None, 'uint16', 'mV'],
                    'SpecificationInfo':      ['word', 0x1A, None, 'uint16', ''],
                    'ManufactureDate':        ['word', 0x1B, None, 'uint16', ''], # ManufacturerDate() value in the following format: Day + Month*32 + (Year–1980)*512
                    'SerialNumber':           ['word', 0x1C, None, 'uint16', 'flags'],
                    'ManufacturerName':       ['block', 0x20, None, 'string', ''],
                    'DeviceName':             ['block', 0x21, None, 'string', ''],
                    'DeviceChemistry':        ['block', 0x22, None, 'string', ''],
                    'ManufacturerData':       ['block', 0x23, None, 'string', ''],
                    'CellVoltage4':           ['word', 0x3C, None, 'uint16', 'mV'],
                    'CellVoltage3':           ['word', 0x3D, None, 'uint16', 'mV'],
                    'CellVoltage2':           ['word', 0x3E, None, 'uint16', 'mV'],
                    'CellVoltage1':           ['word', 0x3F, None, 'uint16', 'mV'],
                    'BTPDischargeSet':        ['word', 0x4A, None, 'int16', 'mAh'],
                    'BTPChargeSet':           ['word', 0x4B, None, 'int16', 'mAh'],
                    'State-of-health':        ['word', 0x4F, None, 'uint8', '%'],
                    'SafetyAlert':            ['block', 0x50, None, 'uint32', 'flags'],
                    'SafetyStatus':           ['block', 0x51, None, 'uint32', 'flags'],
                    'PFAlert':                ['block', 0x52, None, 'uint32', 'flags'],
                    'PFStatus':               ['block', 0x53, None, 'uint32', 'flags'],
                    'OperationStatus':        ['block', 0x54, None, 'uint32', 'flags'],
                    'ChargingStatus':         ['block', 0x55, None, 'uint32', 'flags'],
                    'GaugingStatus':          ['block', 0x56, None, 'uint32', 'flags'],
                    'ManufacturingStatus':    ['word', 0x57, None, 'uint32', 'flags'],
                    'AFERegister':            ['block', 0x58, None, 'uint32', 'flags'],
                    'MaxTurboPwr':            ['word', 0x59, None, 'uint16', 'cW'],
                    'SusTurboPwr':            ['word', 0x5A, None, 'uint16', 'cW'],
                    'TURBO_PACK_R':           ['word', 0x5B, None, 'uint16', 'mOhm'],
                    'TURBO_SYS_R':            ['word', 0x5C, None, 'uint16', 'mOhm'],
                    'TURBO_EDV':              ['word', 0x5D, None, 'uint16', 'mV'],
                    'MaxTurboCurr':           ['word', 0x5E, None, 'uint16', 'mA'],
                    'SusTurboCurr':           ['word', 0x5F, None, 'uint16', 'mA'],
                    'LifeTimeDataBlock1':     ['block', 0x60, None, '-', 'flags'],
                    'LifeTimeDataBlock2':     ['block', 0x61, None, '-', 'flags'],
                    'LifeTimeDataBlock3':     ['block', 0x62, None, '-', 'flags'],
                    'LifeTimeDataBlock4':     ['block', 0x63, None, '-', 'flags'],
                    'LifeTimeDataBlock5':     ['block', 0x64, None, '-', 'flags'],
                    'ManufacturerInfo':       ['block', 0x70, None, '-', 'flags'],
                    'DAStatus1':             ['block', 0x71, None, '-', 'flags'],
                    'DAStatus2':             ['block', 0x72, None, '-', 'flags'],
                    'GaugeStatus1':         ['block', 0x73, None, '-', 'flags'],
                    'GaugeStatus2':         ['block', 0x74, None, '-', 'flags'],
                    'GaugeStatus3':         ['block', 0x75, None, '-', 'flags'],
                    'CBStatus':            ['block', 0x76, None, '-', 'flags'],
                    'STH':                 ['block', 0x77, None, '-', 'flags'],
                    'FilteredCapacity':    ['block', 0x78, None, '-', 'flags']}
        
        self.DataFlash_PermFail = {'SUV_Threshold':             ['Threshold',       0x49C3, None, 'int16', 'mV'],
                                   'SUV_Delay':                 ['Delay',           0x49C5, None, 'uint8', 's'],
                                   'SOV_Threshold':             ['Threshold',       0x49C6, None, 'int16', 'mV'],
                                   'SOV_Delay':                 ['Delay',           0x49C8, None, 'uint8', 's'],
                                   'SOCC_Threshold':            ['Threshold',       0x49C9, None, 'int16', 'mA'],
                                   'SOCC_Delay':                ['Delay',           0x49CB, None, 'uint8', 's'],
                                   'SOCD_Threshold':            ['Threshold',       0x49CC, None, 'int16', 'mA'],
                                   'SOCD_Delay':                ['Delay',           0x49CE, None, 'uint8', 's'],
                                   'SOT_Threshold':             ['Threshold',       0x49CF, None, 'int16', '0.1*K'],
                                   'SOT_Delay':                 ['Delay',           0x49D1,  None,'uint8', 's'],
                                   'SOTF_Threshold':            ['Threshold',       0x49D2, None, 'int16', '0.1*K'],
                                   'SOTF_Delay':                ['Delay',           0x49D4, None, 'uint8', 's'],
                                   'Open_Thermistor_Threshold': ['Threshold',       0x49D5, None, 'int16', '0.1*K'],
                                   'Open_Thermistor_Delay':     ['Delay',           0x49D7, None,  'uint8', 's'],
                                   'Open_Thermistor_Fet_Delta': ['Fet_Delta',       0x49D8, None, 'int16', '0.1*K'],
                                   'Open_Thermistor_Cell_Delta':['Cell_Delta',      0x49DA,None,  'int16', '0.1*K'],
                                   'QIM_Delta_Threshold':       ['Delta_Threshold', 0x49DC,None,  'int16', '0.1%'],
                                   'QIM_Delay':                 ['Delay',           0x49DE,None,  'uint8', 'updates'],
                                   'CB_Max_Threshold':          ['Max_Threshold',   0x49DF,None,  'int16', '2 h'],
                                   'CB_Delta_Threshold':        ['Delta_Threshold', 0x49E1,None,  'uint8', '2 h'],
                                   'CB_Delay':                  ['Delay',           0x49E2, None, 'uint8', 'cycles'],
                                   'VIMR_Check_Voltage':        ['Check_Voltage',   0x49E3, None, 'int16', 'mV'],
                                   'VIMR_Check_Current':        ['Check_Current',   0x49E5, None, 'int16', 'mA'],
                                   'VIMR_Delta_Threshold':      ['Delta_Threshold', 0x49E7,None,  'int16', 'mV'],
                                   'VIMR_Delta_Delay':          ['Delta_Delay',     0x49E9, None, 'uint8', 's'],
                                   'VIMR_Duration':             ['Duration',        0x49EA, None, 'uint16', 's'],
                                   'VIMA_Check_Voltage':        ['Check_Voltage',   0x49EC, None, 'int16', 'mV'],
                                   'VIMA_Check_Current':        ['Check_Current',   0x49EE, None, 'int16', 'mA'],
                                   'VIMA_Delta_Threshold':      ['Delta_Threshold', 0x49F0, None, 'int16', 'mV'],
                                   'VIMA_Delay':                ['Delay',           0x49F2, None, 'uint8', 's'],
                                   'IMP_Delta_Threshold':       ['Delta_Threshold', 0x49F3,None,  'int16', '%'],
                                   'IMP_Max_Threshold':         ['Max_Threshold',   0x49F5, None, 'int16', '%'],
                                   'IMP_Ra_Update_Counts':      ['Ra_Update_Counts',0x49F7, None, 'uint8', 'counts'],
                                   'CD_Threshold':              ['Threshold',       0x49F8,None,  'int16', 'mAh'],
                                   'CD_Delay':                  ['Delay',           0x49FA, None, 'uint8', 'cycles'],
                                   'CFET_OFF_Threshold':        ['OFF_Threshold',   0x49FB,None,  'int16', 'mA'],
                                   'CFET_OFF_Delay':            ['OFF_Delay',       0x49FD, None, 'uint8', 's'],
                                   'DFET_OFF_Threshold':        ['OFF_Threshold',   0x49FE, None,  'int16', 'mA'],
                                   'DFET_OFF_Delay':            ['OFF_Delay',       0x4A00, None,  'uint8', 's'],
                                   'FUSE_Threshold':            ['Threshold',       0x4A01, None,  'int16', 'mA'],
                                   'FUSE_Delay':                ['Delay',           0x4A03, None, 'uint8', 's'],
                                   'AFER_Threshold':            ['Threshold',       0x4A04, None,  'uint8', 's'],
                                   'AFER_Delay_Period':         ['Delay_Period',    0x4A05, None, 'uint8', 's'],
                                   'AFER_Compare_Period':       ['Compare_Period',  0x4A06, None, 'uint8', 's'],
                                   'AFEC_Threshold':            ['Threshold',       0x4A07, None, 'uint8', 's'],
                                   'AFEC_Delay_Period':         ['Delay_Period',    0x4A08, None, 'uint8', 's'],
                                   '2LVL':                      ['Delay',           0x4A09, None, 'uint8', 's']}

    def to_signed_int(self, bytes):
        num = int(bytes[1] + bytes[0], 16)
        if num >= 2**15:
            num -= 2**16
        return num               
                                    
    # print values in reg_dict
    # like this: register name (key): value[2] (value) value[-1] (unit)
    def print_values(self):
        for key, value in self.reg_dict.items():
            if value[0] == 'word':
                if value[-1] == 'flags':
                    print(f'{key}: {value[2]} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
            else:
                if value[-2] == 'string':
                    string_from_reg = ''.join(chr(int(i, 16)) for i in value[2])
                    print(f'{key}: {string_from_reg}')
                else:
                    print(f'{key}: {value[2]} {value[-1]}')
    
    
    
    def read_from_battery(self):
        super().read_SBS_from_battery(self.reg_dict)

    def read_Permanent_Fail_Dataflash(self):
        super().write_block(0x44, [0x49, 0xC3])
        time.sleep(0.1)
        # read 1st block
        # DC = Datachunk
        DC1 = super().read_block(0x44)
        # remove first 3 bytes
        DC1 = DC1[3:]
        time.sleep(0.1)
        # read 2nd block
        DC2 = super().read_block(0x44)
        # remove first 3 bytes
        DC2 = DC2[3:]
        time.sleep(0.1)
        # read 3rd block
        DC3 = super().read_block(0x44)
        # remove first 3 bytes
        DC3 = DC3[3:]
        # now only take first 6 bytes of DC3
        DC3 = DC3[:7]
        # combine all 3 blocks
        DC = DC1 + DC2 + DC3
        # Add the data from DC to the value in index 2 of the dataflash_permFail dict
        for key, value in self.DataFlash_PermFail.items():
            # if value[-2] is uinnt16 or int16, then take 2 bytes from DC
            # else take 1 byte from DC
            index = value[1]-0x49C3
            if value[-2] == 'uint16' or value[-2] == 'int16':
                value[2] = DC[index:index+2]
            else:
                value[2] = DC[index]

    def print_PF_dataflash_values(self):
        for key, value in self.DataFlash_PermFail.items():
            if value[-2] == 'uint16' or value[-2] == 'int16':
                if value[-2] == 'int16':
                    # then the value is siged in 2's complement, so convert it to int
                    print(f'{key}: {self.to_signed_int(value[2])} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][1]+value[2][0],16)} {value[-1]}')
            else:
                # inside value[2] is just a list with a single value for example: ['0x0A']
                # convert it to int and print
                print(f'{key}: {int("00"+value[2],16)} {value[-1]}')


class BQ3060(battery_gauge):
# init function
    def __init__(self):
        super().__init__()
        self.reg_dict = { 'RemainingCapacityAlarm': ['word', 0x01, None, 'uint16', 'mAh'],
                    'RemainingTimeAlarm':     ['word', 0x02, None, 'uint16', 'min'],
                    'BatteryMode':            ['word', 0x03, None, 'uint16', 'flags'],
                    'AtRate':                 ['word', 0x04, None, 'int16', 'mA'],
                    'AtRateTimeToFull':       ['word', 0x05, None, 'uint16', 'min'],
                    'AtRateTimeToEmpty':      ['word', 0x06, None, 'uint16', 'min'],
                    'AtRateOK':               ['word', 0x07, None, 'uint8', ''],
                    'Temperature':            ['word', 0x08, None, 'int16', '0.1*K'],
                    'Voltage':                ['word', 0x09, None, 'uint16', 'mV'],
                    'Current':                ['word', 0x0A, None, 'int16', 'mA'],
                    'AverageCurrent':         ['word', 0x0B, None, 'int16', 'mA'],
                    'MaxError':               ['word', 0x0C, None, 'uint8', 'mA'],
                    'RelativeStateOfCharge':  ['word', 0x0D, None, 'uint8', '%'],
                    'AbsoluteStateOfCharge':  ['word', 0x0E, None, 'uint8', '%'],
                    'RemainingCapacity':      ['word', 0x0F, None, 'uint16', 'mAh'],
                    'FullChargeCapacity':     ['word', 0x10, None, 'uint16', 'mAh'],
                    'RunTimeToEmpty':         ['word', 0x11, None, 'uint16', 'min'],
                    'AverageTimeToEmpty':     ['word', 0x12, None, 'uint16', 'min'],
                    'AverageTimeToFull':      ['word', 0x13, None, 'uint16', 'min'],
                    'ChargingCurrent':        ['word', 0x14, None, 'uint16', 'mA'],
                    'ChargingVoltage':        ['word', 0x15, None, 'uint16', 'mV'],
                    'BatteryStatus':          ['word', 0x16, None, 'uint16', 'flags'],
                    'CycleCount':             ['word', 0x17, None, 'uint16', ''],
                    'DesignCapacity':         ['word', 0x18, None, 'uint16', 'mAh'],
                    'DesignVoltage':          ['word', 0x19, None, 'uint16', 'mV'],
                    'SpecificationInfo':      ['word', 0x1A, None, 'uint16', ''],
                    'ManufactureDate':        ['word', 0x1B, None, 'uint16', ''], # ManufacturerDate() value in the following format: Day + Month*32 + (Year–1980)*512
                    'SerialNumber':           ['word', 0x1C, None, 'uint16', ''],
                    'ManufacturerName':       ['block', 0x20, None, 'string', ''],
                    'DeviceName':             ['block', 0x21, None, 'string', ''],
                    'DeviceChemistry':        ['block', 0x22, None, 'string', ''],
                    'ManufacturerData':       ['block', 0x23, None, 'string', ''],
                    'CellVoltage4':           ['word', 0x3C, None, 'uint16', 'mV'],
                    'CellVoltage3':           ['word', 0x3D, None, 'uint16', 'mV'],
                    'CellVoltage2':           ['word', 0x3E, None, 'uint16', 'mV'],
                    'CellVoltage1':           ['word', 0x3F, None, 'uint16', 'mV'],
                    'State-of-health':        ['word', 0x4F, None, 'uint8', '%'],
                    'SafetyAlert':            ['word', 0x50, None, 'uint16', 'flags'],
                    'SafetyStatus':           ['word', 0x51, None, 'uint16', 'flags'],
                    'PFAlert':                ['word', 0x52, None, 'uint16', 'flags'],
                    'PFStatus':               ['word', 0x53, None, 'uint16', 'flags'],
                    'OperationStatus':        ['word', 0x54, None, 'uint16', 'flags'],
                    'ChargingStatus':         ['word', 0x55, None, 'uint16', 'flags'],
                    'ResetData':              ['word', 0x57, None, 'uint16', 'flags'],
                    'WDResetData':            ['word', 0x58, None, 'uint16', 'flags'],
                    'PackVoltage':            ['word', 0x5A, None, 'uint16', 'mV'],
                    'AverageVoltage':         ['word', 0x5D, None, 'uint16', 'mV'],
                    'UnSealKey':              ['block', 0x60, None, 'uint32', 'flags'],
                    'FullAccessKey':          ['block', 0x61, None, 'uint32', 'flags'],
                    'PFKey':                  ['block', 0x62, None, 'uint32', 'flags'],
                    'AuthenKey3':             ['block', 0x63, None, 'uint32', 'flags'],
                    'AuthenKey2':             ['block', 0x64, None, 'uint32', 'flags'],
                    'Authenkey1':             ['block', 0x65, None, 'uint32', 'flags'],
                    'AuthenKey0':             ['block', 0x66, None, 'uint32', 'flags'],
                    'ManufacturerInfo':       ['block', 0x70, None, 'string', 'flags'],
                    'SenseResistor':          ['block', 0x71, None, 'uint16', 'flags'],
                    'TempRange':              ['block', 0x72, None, 'uint16', 'flags'],
                    'DataFlashSubClassISize': ['block', 0x77, None, 'uint16', 'flags'],
                    'DataFlashSubClassPage1': ['block', 0x78, None, 'H32', 'flags'],
                    'DataFlashSubClassPage2': ['block', 0x79, None, 'H32', 'flags'],
                    'DataFlashSubClassPage3': ['block', 0x7A, None, 'H32', 'flags'],
                    'DataFlashSubClassPage4': ['block', 0x7B, None, 'H32', 'flags'],
                    'DataFlashSubClassPage5': ['block', 0x7C, None, 'H32', 'flags'],
                    'DataFlashSubClassPage6': ['block', 0x7D, None, 'H32', 'flags'],
                    'DataFlashSubClassPage7': ['block', 0x7E, None, 'H32', 'flags'],
                    'DataFlashSubClassPage8': ['block', 0x7F, None, 'H32', 'flags']}
    
        self.first_level_safety_dict = {'LT COV Threshold':     ['Voltage', 'I2', None, 'mV'], 
                                      'LT COV Recovery':        ['Voltage', 'I2', None, 'mV'], 
                                      'ST COV Threshold':       ['Voltage', 'I2', None, 'mV'], 
                                      'ST COV Recovery':        ['Voltage', 'I2', None, 'mV'], 
                                      'HT COV Threshold':       ['Voltage', 'I2', None, 'mV'], 
                                      'HT COV Recovery':        ['Voltage', 'I2', None, 'mV'], 
                                      'CUV Threshold':          ['Voltage', 'I2', None, 'mV'], 
                                      'CUV Recovery':           ['Voltage', 'I2', None, 'mV'], 
                                      'OC (1st Tier) Chg':      ['Current', 'I2', None, 'mA'],
                                      'OC (1st Tier) Chg Time': ['Current', 'U1', None, 's'], 
                                      'OC Chg Recovery':        ['Current', 'I2', None, 'mA'], 
                                      'OC (1st Tier) Dsg':      ['Current', 'I2', None, 'mA'], 
                                      'OC (1st Tier) Dsg Time': ['Current', 'U1', None, 's'], 
                                      'OC Dsg Recovery':        ['Current', 'I2', None, 'mA'], 
                                      'Current Recovery Time':  ['Current', 'U1', None, 's'], 
                                      'AFE OC Dsg':             ['Current', 'H1', None, None],
                                      'AFE OC Dsg Time':        ['Current', 'H1', None, None], 
                                      'AFE OC Dsg Recovery':    ['Current', 'I2', None, 'mA'],
                                      'AFE SC Chg Cfg':         ['Current', 'H1', None, None], 
                                      'AFE SC Dsg Cfg':         ['Current', 'H1', None, None], 
                                      'AFE SC Recovery':        ['Current', 'I2', None, 'mA'],
                                      'Over Temp Chg':          ['Temperature', 'I2',None,  '0.1°C'], 
                                      'OT Chg Time':            ['Temperature', 'U1',None,  's'],
                                      'OT Chg Recovery':        ['Temperature', 'I2',None,  '0.1°C'], 
                                      'Over Temp Dsg':          ['Temperature', 'I2',None,  '0.1°C'],
                                      'OT Dsg Time':            ['Temperature', 'U1',None,  's'],
                                      'OT Dsg Recovery':        ['Temperature', 'I2',None,  '0.1°C']}

    def to_signed_int(self, bytes):
        num = int(bytes[1] + bytes[0], 16)
        if num >= 2**15:
            num -= 2**16
        return num    
    # print values in reg_dict
    # like this: register name (key): value[2] (value) value[-1] (unit)
    def print_values(self):
        for key, value in self.reg_dict.items():
            if value[0] == 'word':
                if value[-1] == 'flags':
                    print(f'{key}: {value[2]} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
            else:
                print(f'{key}: {value[2]} {value[-1]}')
    
    # print values in reg_dict
    # like this: register name (key): value[2] (value) value[-1] (unit)
    def print_values(self):
        for key, value in self.reg_dict.items():
            if value[0] == 'word':
                if value[-1] == 'flags':
                    print(f'{key}: {value[2]} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
            else:
                if value[-2] == 'string':
                    string_from_reg = ''.join(chr(int(i, 16)) for i in value[2])
                    print(f'{key}: {string_from_reg}')
                else:
                    print(f'{key}: {value[2]} {value[-1]}')
    
    def read_from_battery(self):
        super().read_SBS_from_battery(self.reg_dict)

    def read_1st_level_safety(self):

        time.sleep(0.1)
        super().write_word(0x77, [0x00, 0x00])
        time.sleep(0.1)

        # read 1st block
        # DC = Datachunk

        time.sleep(0.1)
        DC1 = super().read_block(0x78)
        time.sleep(0.1)
        # remove first 1 bytes
        print("DC1: ", DC1)
        DC1 = DC1[1:]

        time.sleep(0.1)
        super().write_word(0x77, [0x01, 0x00])
        time.sleep(0.1)

        # read 2nd block
        time.sleep(0.1)
        DC2 = super().read_block(0x78)
        time.sleep(0.1)

        print("DC2: ", DC2)
        DC2 = DC2[1:]

        time.sleep(0.1)
        super().write_word(0x77, [0x02, 0x00])
        time.sleep(0.1)

        # read 3rd block
        time.sleep(0.1)
        DC3 = super().read_block(0x78)
        print("DC3: ", DC3)
        DC3 = DC3[1:]
        DC = DC1 + DC2 + DC3
        # Add the data from DC to the value in index 2 of the dataflash_permFail dict
        i = 0
        print("DC: ", DC)
        print("len(DC): ", len(DC))
        for key, value in self.first_level_safety_dict.items():
            if value[1] == 'I2':
                value[2] = DC[i:i+2]
                i += 2
            else:
                value[2] = DC[i]
                i += 1
    
    def print_1st_level_safety_dataflash_value(self):
        for key, value in  self.first_level_safety_dict.items():
            if value[1] == 'I2':
                print(f'{key}: {self.to_signed_int(value[2])} {value[-1]}')
            else:
                # inside value[2] is just a list with a single value for example: ['0x0A']
                # convert it to int and print
                print(f'{key}: {int("00"+value[2],16)} {value[-1]}')



# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])



if len(sys.argv) > 1:
    if sys.argv[1] == "BQ4050":
        current_battery= BQ4050()
        if sys.argv[2] == "0":
            current_battery.read_from_battery()
            current_battery.print_values()
        elif sys.argv[2] == "1":
            current_battery.read_Permanent_Fail_Dataflash()
            current_battery.print_PF_dataflash_values() 
    if sys.argv[1] == "BQ3060":
        current_battery= BQ3060()
        time.sleep(0.1)
        if sys.argv[2] == "0":
            current_battery.read_from_battery()
            current_battery.print_values()
        elif sys.argv[2] == "1":
            current_battery.read_1st_level_safety()
            current_battery.print_1st_level_safety_dataflash_value()


    #print(current_battery.DataFlash_PermFail)

