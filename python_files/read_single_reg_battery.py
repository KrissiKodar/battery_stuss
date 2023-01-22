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
ManufacturingStatus = 0x57
BatteryMode = 0x03
BatteryStatus = 0x16
OperationStatus = 0x54


# read from the serial port and print the data
# the port is COM6 in my case
ser = serial.Serial('COM5', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

# convert list of hex values into one decimal value
def hex_to_dec(data):
    # if data is empty return 0
    if not data:
        return 0
    return int(''.join(data), 16)


# function that convert list of hex values into full binary string (register value)
def hex_to_bin(data):
    if not data:
        return 0
    return ''.join(format(int(x, 16), '08b') for x in data)

# Extract each byte as is and put it in a list
def data_to_list(data):
    ascii_list = [data[i:i+1] for i in range(0, len(data), 1)]
    ascii_list  = [x.decode('ascii') for x in ascii_list ]
    return ascii_list 

def user_input_processing(user_input):
    if user_input == '1':
        return tempAddress
    elif user_input == '2':
        return voltageAddress
    elif user_input == '3':
        return currentAddress
    elif user_input == '4':
        return averageCurrentAddress
    elif user_input == '5':
        return maxErrorAddress
    elif user_input == '6':
        return relativeStateOfChargeAddress
    elif user_input == '7':
        return absoluteStateOfChargeAddress
    elif user_input == '8':
        return remainingCapacityAddress
    elif user_input == '9':
        return fullChargeCapacityAddress
    elif user_input == '10':
        return runTimeToEmpty
    elif user_input == '11':
        return runTimeToFull
    elif user_input == '12':
        return ManufacturingStatus
    elif user_input == '13':
        return BatteryMode
    elif user_input == '14':
        return BatteryStatus
    elif user_input == '15':
        return OperationStatus
    else:
        return 0

def print_results(user_input, data):
    if user_input == '1':
        new_data = hex_to_dec(data_to_list(data)) # in 0.1 K
        new_data = round(new_data*0.1- 273.15, 1)
        print(f'Temperature: {new_data} C')
        return
    elif user_input == '2':
        print(f'Voltage: {hex_to_dec(data_to_list(data))} mV')
        return
    elif user_input == '3':
        print(f'Current: {hex_to_dec(data_to_list(data))} mA')
        return
    elif user_input == '4':
        print(f'Average Current: {hex_to_dec(data_to_list(data))} mA')
        return
    elif user_input == '5':
        print(f'Max Error: {hex_to_dec(data_to_list(data))} %')
        return
    elif user_input == '6':
        print(f'Relative State of Charge: {hex_to_dec(data_to_list(data))} %')
        return
    elif user_input == '7':
        print(f'Absolute State of Charge: {hex_to_dec(data_to_list(data))} %')
        return
    elif user_input == '8':
        print(f'Remaining Capacity: {hex_to_dec(data_to_list(data))} mAh')
        return
    elif user_input == '9':
        print(f'Full Charge Capacity: {hex_to_dec(data_to_list(data))} mAh')
        return
    elif user_input == '10':
        print(f'Run Time to Empty: {hex_to_dec(data_to_list(data))} min')
        return
    elif user_input == '11':
        print(f'Run Time to Full: {hex_to_dec(data_to_list(data))} min')
        return
    elif user_input == '12':
        print(f'Manufacturing Status: {hex_to_dec(data_to_list(data))}')
        return
    elif user_input == '13':
        print(f'Battery Mode: {hex_to_dec(data_to_list(data))}')
        return
    elif user_input == '14':
        print(f'Battery Status: {hex_to_dec(data_to_list(data))}')
        return
    elif user_input == '15':
        print(f'Operation Status: {hex_to_bin(data_to_list(data))}')
        print(f'len: {len(hex_to_bin(data_to_list(data)))}')
    else:
        print('Invalid input')
        return 0




# write the address of the register you want to read
while True:
    print('1. Temperature')
    print('2. Voltage')
    print('3. Current')
    print('4. Average Current')
    print('5. Max Error')
    print('6. Relative State of Charge')
    print('7. Absolute State of Charge')
    print('8. Remaining Capacity')
    print('9. Full Charge Capacity')
    print('10. Run Time to Empty')
    print('11. Run Time to Full')
    print('12. Manufacturing Status')
    print('13. Battery Mode')
    print('14. Battery Status')
    print('15. Operation Status')
    #a = ser.write(b'\x09')
    # ask for user input
    
    # empty bytearray
    empy_bytearray = bytearray()
    
    user_input = input('Enter the address of the register you want to read: ')

    print(f'user input: {user_input}')
    print(f'user input after processing: {user_input_processing(user_input)}')

    a = ser.write(user_input_processing(user_input).to_bytes(1, byteorder='big'))
    print(f'write {a} bytes')
    time.sleep(0.5)
    # read all bytes available
    data = ser.read(ser.in_waiting)
    #print(f'read {len(data)} bytes')
    time.sleep(0.1)
    print(len(data))
    #print(data)
    
    # flip the bytes
    data = data[::-1]
    
    print(data)
    
    
    # if length of data is 4 bytes, the bytes are in little endian format
    # make them big endian
    
    # for example instead of printint b'\x03\x20\x01\x07' print 0x03200107
    print(''.join(format(x, '02x') for x in data))
    
    # print in binary format
    print(''.join(format(x, '08b') for x in data))
    
    # print in decimal format
    print(int.from_bytes(data, byteorder='big'))
    
    # b'' is in hex format
    # print data with leading zeros if needed
    print(type(data))
    #print_results(user_input, data)
    # wait until user presses enter
    input('Press enter to continue')
    # clear terminal
    print('\033c')