import serial
from serial.tools import list_ports
import time
port = list(list_ports.comports())
print(port)
for p in port:
    print(p.device)

tempAddress = 0x08
voltageAddress = 0x09
currentAddress = 0x0A
averageCurrentAddress = 0x0B
maxErrorAddress = 0x0C
relativeStateOfChargeAddress = 0x0D
absoluteStateOfChargeAddress = 0x0E
remainingCapacityAddress = 0x0F
fullChargeCapacityAddress = 0x10
runTimeToEmpty = 0x11
runTimeToFull = 0x12



# all of the registers for the battery (BQ40Z50-R2)
# Lets store it like name, hex address, type, bytes, units (if applicable)

# q: what would be the best way to store this data?
# a: I think a dictionary would be the best way to store this data


reg_dict = {'RemainingCapacityAlarm': [0x01, 'uint16', 'mAh'],
            'RemainingTimeAlarm':     [0x02, 'uint16', 'min'],
            'BatteryMode':            [0x03, 'uint16', 'flags'],
            'AtRate':                 [0x04, 'int16', 'mA'],
            'AtRateTimeToFull':       [0x05, 'uint16', 'min'],
            'AtRateTimeToEmpty':      [0x06, 'uint16', 'min'],
            'AtRateOK':               [0x07, 'uint8', ''],
            'Temperature':            [0x08, 'int16', 'K'],
            'Voltage':                [0x09, 'uint16', 'mV'],
            'Current':                [0x0A, 'int16', 'mA'],
            'AverageCurrent':         [0x0B, 'int16', 'mA'],
            'MaxError':               [0x0C, 'uint8', 'mA'],
            'RelativeStateOfCharge':  [0x0D, 'uint8', '%'],
            'AbsoluteStateOfCharge':  [0x0E, 'uint8', '%'],
            'RemainingCapacity':      [0x0F, 'uint16', 'mAh'],
            'FullChargeCapacity':     [0x10, 'uint16', 'mAh'],
            'RunTimeToEmpty':         [0x11, 'uint16', 'min'],
            'AverageTimeToEmpty':     [0x12, 'uint16', 'min'],
            'AverageTimeToFull':      [0x13, 'uint16', 'min'],
            'ChargingCurrent':        [0x14, 'uint16', 'mA'],
            'ChargingVoltage':        [0x15, 'uint16', 'mV'],
            'BatteryStatus':          [0x16, 'uint16', 'flags'],
            'CycleCount':             [0x17, 'uint16', ''],
            'DesignCapacity':         [0x18, 'uint16', 'mAh'],
            'DesignVoltage':          [0x19, 'uint16', 'mV'],
            'SpecificationInfo':      [0x1A, 'uint16', ''],
            'ManufactureDate':        [0x1B, 'uint16', ''], # ManufacturerDate() value in the following format: Day + Month*32 + (Year–1980)*512
            'SerialNumber':           [0x1C, 'uint16', ''],
            'CellVoltage4':           [0x3C, 'uint16', 'mV'],
            'CellVoltage3':           [0x3D, 'uint16', 'mV'],
            'CellVoltage2':           [0x3E, 'uint16', 'mV'],
            'CellVoltage1':           [0x3F, 'uint16', 'mV'],
            'BTPDischargeSet':        [0x4A, 'int16', 'mAh'],
            'BTPChargeSet':           [0x4B, 'int16', 'mAh'],
            'State-of-health':        [0x4F, 'uint8', '%'],
            'SafetyAlert':            [0x50, 'uint32', 'flags'],
            'SafetyStatus':           [0x51, 'uint32', 'flags'],
            'PFAlert':                [0x52, 'uint32', 'flags'],
            'PFStatus':               [0x53, 'uint32', 'flags'],
            'OperationStatus':        [0x54, 'uint32', 'flags'],
            'ChargingStatus':         [0x55, 'uint32', 'flags'],
            'GaugingStatus':          [0x56, 'uint32', 'flags'],
            'ManufacturingStatus':    [0x57, 'uint32', 'flags']}
            


bytes_requested = [2,2,2,2,2,2,1,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,4,4,4,4,4,4,4,4]
        
# veit ekki hvad a ad gera med registera 0x58 og upp eda  'ManufacturerData':       [0x23, 'mixed', ''], mixed ???

# sma ves med thetta
#            'ManufacturerName':       [0x20, 'S20+1', ''],# S20+1---> 20 bytes of data + 1 byte of checksum
#            'DeviceName':             [0x21, 'S20+1', ''],      # S20+1---> 20 bytes of data + 1 byte of checksum
#            'DeviceChemistry':        [0x22, 'S4+1', ''], # S4+1 --->  4 bytes of data + 1 byte of checksum
#            'Authenticate':           [0x2F, 'H20+1', ''], # H20 + 1: ---> 20 bytes of data + 1 byte of checksum

all_reg= [0x01 ,0x02 ,0x03 ,0x04 ,0x05 ,0x06 ,0x07 ,0x08 ,0x09 ,0x0A ,0x0B ,0x0C ,0x0D ,0x0E ,0x0F ,0x10,
          0x11 ,0x12 ,0x13 ,0x14 ,0x15 ,0x16 ,0x17 ,0x18 ,0x19 ,0x1A ,0x1B ,0x1C,
          0x3C ,0x3D ,0x3E ,0x3F ,0x4A ,0x4B ,0x4F ,0x50 ,0x51 ,0x52 ,0x53 ,0x54 ,0x55 ,0x56 ,0x57]

#all_reg= [0x01 ,0x02 ,0x03 ,0x04 ,0x05 ,0x06 ,0x07 ,0x08 ,0x09 ,0x0A ,0x0B ,0x0C ,0x0D ,0x0E ,0x0F ,0x10,
#          0x11 ,0x12 ,0x13 ,0x14 ,0x15 ,0x16 ,0x17 ,0x18 ,0x19 ,0x1A ,0x1B ,0x1C ,0x20 ,0x21 ,0x22 ,0x2F,
#          0x3C ,0x3D ,0x3E ,0x3F ,0x4A ,0x4B ,0x4F ,0x50 ,0x51 ,0x52 ,0x53 ,0x54 ,0x55 ,0x56 ,0x57]


total_bytes = sum(bytes_requested)
print(total_bytes)


HandshakeRequest =   bytes([0x3D, 0x00, 0x02, 0x01, 0x00, 0x03])
ExpectedHandshake =  bytes([0x3D, 0x00, 0x08, 0x81, 0x00, 0x53, 0x42, 0x48, 0x41, 0x43, 0x4B, 0x35])

print(f'HandshakeRequest: {HandshakeRequest}')

ser = serial.Serial('COM5', 250000, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

dump_all = [0x3D, 0x00, 0x04, 0x02, 0x03, 0x00, 0x78, 0x81]

# send the handshake request, try 5 times, if no response, exit terminal
def handshake(requested, expected):
    # conver requested and expected to bytes
    for i in range(5):
        received = []
        ser.write(requested, )
        time.sleep(2)
        num_bytes = ser.inWaiting()
        print(f'num_bytes: {num_bytes}')
        for i in range(num_bytes):
            received.append(ser.read(1))
        if received == expected:
            return True
        else:
            # convert received to pure hex
            received = [hex(i[0]) for i in received]
            print(f'received: {received}')
            return False
            
    


if handshake(HandshakeRequest, ExpectedHandshake):
    user_input = input('press 1 to read all: ')
    # ser write the dump_all list, which is the command to dump all registers

    data_list = []

    ser.write(dump_all)

    time.sleep(2)

    # number of bytes to read from the serial port
    num_bytes = ser.inWaiting()
    print(f'num_bytes: {num_bytes}')
    # read all bytes one by one in to data_list
    for i in range(num_bytes):
        data_list.append(ser.read(1))


    print(f'data_list: {data_list}')


    #print(f'data_list: {data_list}')d
