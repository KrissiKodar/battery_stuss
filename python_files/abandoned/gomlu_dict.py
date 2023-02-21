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
                    'SenseResistor':          ['word',  0x71, None, 'uint16', 'microOhm'],
                    'TempRange':              ['word',  0x72, None, 'uint16', 'flags'],
                    'DataFlashSubClassISize': ['block', 0x77, None, 'uint16', 'flags'],
                    'DataFlashSubClassPage1': ['block', 0x78, None, 'H32', 'flags'],
                    'DataFlashSubClassPage2': ['block', 0x79, None, 'H32', 'flags'],
                    'DataFlashSubClassPage3': ['block', 0x7A, None, 'H32', 'flags'],
                    'DataFlashSubClassPage4': ['block', 0x7B, None, 'H32', 'flags'],
                    'DataFlashSubClassPage5': ['block', 0x7C, None, 'H32', 'flags'],
                    'DataFlashSubClassPage6': ['block', 0x7D, None, 'H32', 'flags'],
                    'DataFlashSubClassPage7': ['block', 0x7E, None, 'H32', 'flags'],
                    'DataFlashSubClassPage8': ['block', 0x7F, None, 'H32', 'flags']}
    

    # print values in reg_dict
    # print the basic SBS registers
    def print_values(self):
        for key, value in self.reg_dict.items():
            #print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
            #value[2] = int(value[2][0]+value[2][1],16)
            if value[-2] == 'uint16':
                if value[-1] == 'flags':
                    value[2] = self.bytes_to_hex(value[2])
                    print(f'{key}: {value[2]} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
                    value[2] = int(value[2][0]+value[2][1],16)
            elif value[-2] == 'int16':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.to_signed_int(value[2])
            elif value[-2] == 'uint8':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = int(value[2][0],16)
            elif value[-2] == 'int8':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.to_signed_byte(value[2][0])
            elif value[-2] == 'string':
                string_from_reg = ''.join(chr(int(i, 16)) for i in value[2])
                print(f'{key}: {string_from_reg}')
                value[2] = string_from_reg
            elif value[-2] == 'uint32':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.bytes_to_hex(value[2])
            else:
                print(f'{key}: {value[2]} {value[-1]}')


    def read_basic_SBS(self):
        super().read_SBS_from_battery(self.reg_dict)


def return_dict(self):
return self.reg_dict


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
                    'AFERegister':            ['block', 0x58, None, '-', 'flags'],
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




 # print values in reg_dict
    # like this: register name (key): value[2] (value) value[-1] (unit)
    # print values in reg_dict
    # print the basic SBS registers
    def print_values(self):
        for key, value in self.reg_dict.items():
            #print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
            #value[2] = int(value[2][0]+value[2][1],16)
            if value[-2] == 'uint16':
                if value[-1] == 'flags':
                    value[2] = self.bytes_to_hex_SBS(value[2])
                    print(f'{key}: {value[2]} {value[-1]}')
                else:
                    print(f'{key}: {int(value[2][0]+value[2][1],16)} {value[-1]}')
                    value[2] = int(value[2][0]+value[2][1],16)
            elif value[-2] == 'int16':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.to_signed_int_SBS(value[2])
            elif value[-2] == 'uint8':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = int(value[2][0],16)
            elif value[-2] == 'int8':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.to_signed_byte(value[2][0])
            elif value[-2] == 'string':
                string_from_reg = ''.join(chr(int(i, 16)) for i in value[2])
                print(f'{key}: {string_from_reg}')
                value[2] = string_from_reg
            elif value[-2] == 'uint32':
                print(f'{key}: {value[2]} {value[-1]}')
                value[2] = self.bytes_to_hex_SBS(value[2])
            else:
                print(f'{key}: {value[2]} {value[-1]}')



                
    def read_basic_SBS(self):
        super().read_SBS_from_battery(self.reg_dict)


    def return_dict(self):
        return self.reg_dict


    #################################################################################
   
    # specific functions for SBS, because the byte order is big endian
    def to_signed_int_SBS(self, bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num

    def bytes_to_hex_SBS(self, data): # must be even number of bytes >= 2
            # make letters in data upper case
            for i in range(len(data)):
                k = data[i]
                data[i] = k.upper()	
            ret = '0x'
            # append each byte to ret
            for i in range(len(data)):	
                ret += data[i]	
            return ret
    #################################################################################