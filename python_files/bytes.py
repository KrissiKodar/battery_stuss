

def to_signed_int(bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num


# function to convert a single signed byte to int
def to_signed_byte(byte):
    num = int(byte, 16)
    if num >= 2**7:
        num -= 2**8
    return num

value=['0x01','0xFF']
print(int(value[0][2:]+value[1][2:],16))

signed_byte = ['0xFF']
print(to_signed_byte(signed_byte[0]))