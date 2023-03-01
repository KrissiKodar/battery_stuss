# Assuming little endian byte order and IEEE 754 single-precision format
bytes_list = ['82', '3e', 'da', 'd9']
bytes_list = ['da', 'd9','82', '3e']
# flip bytes
#bytes_list.reverse()
#Floating point values are stored using a 4-byte format, where the LSB is the exponent, bytes 1 to 3 are the
#mantissa in unsigned integer format, with the MSB in byte 1 as a signed bit.
# convert bytes to float
# Assuming little endian byte order and IEEE 754 single-precision format
import struct
bytes_obj = bytes.fromhex(''.join(bytes_list)) # Convert hex strings to bytes object
float_val = struct.unpack('f', bytes_obj)[0] # Convert bytes object to float
print(float_val) # Output: 1.7213997840881348e-38