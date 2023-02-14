

def to_signed_int(bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num

# same as bytes to hex but put them in a list
def bytes_to_hex_list(data):
    return [hex(b)[2:].zfill(2) for b in data]

ascii_list = ['00', '01', '00', '00', '0a', '57', '41', '4d', '54', '45', '43', '48', '4e', '49', '4b', '41', '42', '43', '44', '45', '46', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '41']

string_from_reg = ''.join(chr(int(i, 16)) for i in ascii_list)
print(string_from_reg)