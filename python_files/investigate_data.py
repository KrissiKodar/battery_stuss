import pandas as pd
import pickle


# load BQ4050_SBS_saved.pkl
with open('BQ4050_SBS_saved.pkl', 'rb') as file:
    # Load the dictionary back from the pickle file.
    BQ4050_SBS_saved = pickle.load(file)

# print last 30 rows of BQ4050_SBS_saved
print(BQ4050_SBS_saved[-30:])

# print MEASURED VALUE OF NAME OperationStatus
bla =BQ4050_SBS_saved.loc[BQ4050_SBS_saved['NAME'] == 'OperationStatus', 'MEASURED VALUE']
print(bla)
print(type(bla))
bla = list(bla)
print(bla[0])



print(BQ4050_SBS_saved[25:40])
print(BQ4050_SBS_saved[-30:])


""" def bytes_to_hex(data): # must be even number of bytes >= 2
    # make letters in data upper case
    for i in range(len(data)):
        k = data[i]
        data[i] = k.upper()	
    ret = '0x'
    # append each byte to ret
    for i in range(len(data)):	
        ret += data[i]	
    return ret

def to_signed_int_SBS(bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num

def to_signed_byte(byte):
        num = int(byte, 16)
        if num >= 2**7:
            num -= 2**8
        return num    

# if SIZE IN BYTES > 2 the remove first item from MEASURED VALUE list
for index, row in BQ4050_SBS_saved.iterrows():
    if int(row['SIZE IN BYTES']) > 2:
        value = row['MEASURED VALUE']
        # remove first item from list
        value.pop(0)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value

for index, row in BQ4050_SBS_saved.iterrows():
    # if "SIZE IN BYTES" > 3 and "UNIT" is not "ASCII" and "NAME"
    if int(row['SIZE IN BYTES']) > 3 and row['UNIT'] != 'ASCII':
        value = row['MEASURED VALUE']
        # flip order of list elements, first flip first two elements, then the next two, etc.
        if len(value) % 2 == 0:
            print("len(value): ", len(value))
            for i in range(0, len(value), 2):
                value[i], value[i+1] = value[i+1], value[i]
        value = bytes_to_hex(value)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value



# if FORMAT is "integer" and "SIZE IN BYTES" is 2
for index, row in BQ4050_SBS_saved.iterrows():
    if row['FORMAT'] == 'integer' and int(row['SIZE IN BYTES']) == 2:
        value = row['MEASURED VALUE']
        value = to_signed_int_SBS(value)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value
    # if FORMAT is "integer" and "SIZE IN BYTES" is 1
    if row['FORMAT'] == 'integer' and int(row['SIZE IN BYTES']) == 1:
        value = row['MEASURED VALUE']
        value = to_signed_byte(value)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value
    # if FORMAT is "unsigned int" and "SIZE IN BYTES" is 2
    if row['FORMAT'] == 'unsigned int' and int(row['SIZE IN BYTES']) == 2:
        value = row['MEASURED VALUE']
        value = int(value[0]+value[1],16)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value
    # FORMAT is "unsigned int" and "SIZE IN BYTES" is 1
    if row['FORMAT'] == 'unsigned int' and int(row['SIZE IN BYTES']) == 1:
        value = row['MEASURED VALUE']
        value = int(value[1],16)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value

    # if FORMAT is hex and "SIZE IN BYTES" is 2
    if row['FORMAT'] == 'hex' and int(row['SIZE IN BYTES']) == 2:
        value = row['MEASURED VALUE']
        value = bytes_to_hex(value)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = value
    
    # if FORMAT is "string" and UNIT is "ASCII"
    if row['FORMAT'] == 'string' and row['UNIT'] == 'ASCII':
        value = row['MEASURED VALUE']
        string_from_reg = ''.join(chr(int(i, 16)) for i in value)
        # update MEASURED VALUE
        BQ4050_SBS_saved.at[index, 'MEASURED VALUE'] = string_from_reg



 """