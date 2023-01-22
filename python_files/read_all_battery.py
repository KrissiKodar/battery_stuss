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

# read from the serial port and print the data
# the port is COM6 in my case
ser = serial.Serial('COM6', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

# convert list of hex values into one decimal value
def hex_to_dec(data):
    # if data is empty return 0
    if not data:
        return 0
    return int(''.join(data), 16)

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
    #a = ser.write(b'\x09')
    # ask for user input
    user_input = input('Enter the address of the register you want to read: ')

    print(f'user input: {user_input}')
    print(f'user input after processing: {user_input_processing(user_input)}')

    a = ser.write(user_input_processing(user_input).to_bytes(1, byteorder='big'))
    print(f'write {a} bytes\n')
    time.sleep(5)
    # read all bytes available
    data = ser.read(ser.in_waiting)
    print(f'read {len(data)} bytes')
    time.sleep(0.1)
    print(f'data: {data}')
    #print_results(user_input, data)
    # wait until user presses enter
    two_bytes = data_to_list(data)
    # each entry is a nibble
    # put every 4 elements in a new list
    k = 1
    for i in range(0, len(two_bytes), 4):
        new_list = two_bytes[i:i+4]
        print(f'new list: {new_list}')
        print(f'regiser address: {k}')
        print(f'new list after processing: {hex_to_dec(new_list)}')
        k += 1
    input('Press enter to continue')
    # clear terminal
    #print('\033c')