 def read_1st_level_safety(self):

        DELAY = 0.02
        time.sleep(DELAY)
        super().write_word(0x77, [0x00, 0x00])
        time.sleep(DELAY)

        # read 1st block
        # DC = Datachunk

        time.sleep(DELAY)
        DC1 = super().read_block(0x78)
        time.sleep(DELAY)
        # remove first 1 bytes
        print("DC1: ", DC1)
        DC1 = DC1[1:]

        time.sleep(DELAY)
        super().write_word(0x77, [0x01, 0x00])
        time.sleep(DELAY)

        # read 2nd block
        time.sleep(DELAY)
        DC2 = super().read_block(0x78)
        time.sleep(DELAY)

        print("DC2: ", DC2)
        DC2 = DC2[1:]

        time.sleep(DELAY)
        super().write_word(0x77, [0x02, 0x00])
        time.sleep(DELAY)

        # read 3rd block
        time.sleep(DELAY)
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

    def read_all_dataflash(self):

        subclass_ID = [0,1,2,16,17,18,19,20,32,33,34,36,37,38,48,49,56,58,59,64,65,68,85,81,82,96,97,104,105,106,107]
        # subclass_IDs: 34 --> 38 bytes
        # subclass_IDs: 48 --> 55 bytes
        # subclass_IDs: 85 --> 48 bytes
        # subclass_IDs: 96 --> 32 bytes (sleppur held eg)
        # subclass_IDs: 106 --> 38 bytes
        two_reads = [34,48,85,106]

        # subclass ID: number of bytes according to the datasheet for BQ3060
        # bugs = {82: 10, 107: 3, 59: 8, 65: 1}

        #DC = []
        DELAY = 0.02

        for i in subclass_ID:
            time.sleep(DELAY)
            super().write_word(0x77, [i, 0x00])
            time.sleep(DELAY)

            time.sleep(DELAY)
            DC1 = super().read_block(0x78)
            time.sleep(DELAY)
            # remove first 1 bytes (which is just the length of the data)
            DC1 = DC1[1:]
            # if i is a key in bugs, remove the last bytes
            #if i in bugs:
            #    DC1 = DC1[0:bugs[i]]
            
            print(f"subclass ID: {i} first, length = {len(DC1)}", DC1)


            if i in two_reads:
                time.sleep(DELAY)
                DC2 = super().read_block(0x79)
                time.sleep(DELAY)
                DC2 = DC2[1:]
                print(f"subclass ID: {i} second, length = {len(DC2)}", DC2)
                DC1.extend(DC2)
            
            # for all keys in dictionry whose value[0] is equal to i
            for key, value in self.data_dict.items():
                if value[0] == str(i):
                    offset = int(value[-2])
                    if len(DC1) == 1:
                        value[2] = DC1[0]
                    elif value[1] in ['S12', 'S32']:
                        value[2] = DC1[offset:offset+int(value[1][1:3])]
                    else:
                        value[2] = DC1[offset:offset+int(value[1][1])]

           
                
        # Add the data from DC to the value in index 2 of the dataflash_permFail dict
        #i = 0
        #print("DC: ", DC)
        #print("len(DC): ", len(DC))
        """ try:
            for key, value in self.data_dict.items():
                if value[1] in ['I2', 'U2', 'H2']:
                    value[2] = DC[i:i+2]
                    i += 2
                elif value[1] in ['S5', 'S8']:
                    value[2] = DC[i:i+int(value[1][1])]
                    i += int(value[1][1])
                    print("String in question: ", value[2])
                elif value[1] in ['S12', 'S32']:
                    value[2] = DC[i:i+int(value[1][1:3])]
                    print("String in question: ", value[2])
                    i += int(value[1][1:3])
                elif value[1] in ['F4']:
                    value[2] = DC[i:i+4]
                    i += 4
                else:
                    value[2] = DC[i]
                    i += 1
        except IndexError:
            print("IndexError")
            print("i: ", i)
            print("key: ", key) """
            
            
def print_dataflash_values(self):
        print(self.data_dict)
        i = 0
        for key, value in  self.data_dict.items():
            if value[1] == 'I2':
                print(f'{key}: {self.to_signed_int_dataflash(value[2])} {value[-1]}')
                i += 1
            elif value[1] == 'U2':
                print(f'{key}: {self.to_unsigned_int_dataflash(value[2])} {value[-1]}')
            elif value[1] == 'H2' or value[1] == 'H1':
                print(f'{key}: {value[2]} {value[-1]}')
            elif value[1] in ['S5', 'S8', 'S12', 'S32']:
                print(value[2])
                string_from_reg = ''.join(chr(int(i, 16)) for i in value[2])
                print(f'{key}: {string_from_reg}')
            elif value[1] == 'F4':
                #print(f'{key}: {self.to_float(value[2])} {value[-1]}')
                print(f'{key}: {value[2]} {value[-1]}')
            else:
                # inside value[2] is just a list with a single value for example: ['0x0A']
                # convert it to int and print
                print(f'{key}: {int("00"+value[2][0],16)} {value[-1]}')
                
                


##### BQ4050 ##### below

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

    def read_dataflash_test(self):
        super().write_block(0x44, [0x46, 0x40])
        
        # read 1st block
        # DC = Datachunk
        DC1 = super().read_block(0x44)
        time.sleep(0.1)
        # remove first 1 bytes
        DC1 = DC1[1:]

        # combine all 3 blocks
        DC = DC1 
        
        print(DC1)
        print("len(DC): ", len(DC1))
        
        DC2 = super().read_block(0x44)
        DC2 = DC2[1:]
        time.sleep(0.1)
        
        print(DC2)
        print("len(DC): ", len(DC2))
        
        DC3 = super().read_block(0x44)
        DC3 = DC3[1:]
        time.sleep(0.1)
        
        print(DC3)
        print("len(DC): ", len(DC3))

    def read_all_dataflash(self):
        super().write_block(0x44, [0x46, 0x00])
        time.sleep(0.1)
        # read 1st block
        # DC = Datachunk
        DC1 = super().read_block(0x44)
        # remove first 3 bytes
        DC1 = DC1[3:]

        # combine all 3 blocks
        DC = DC1 
        
        print(DC)
        print("len(DC): ", len(DC))