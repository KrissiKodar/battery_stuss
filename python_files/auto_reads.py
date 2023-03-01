import serial
from serial.tools import list_ports
from serial import Serial
import sys
import time
import pickle
import pandas as pd
import struct

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc

from batteries import *

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])

# initiate parent class
if __name__ == "__main__":
    ####################### SQL ############################
    my_uid = "LAPTOP-GG7823IL\dadas"
    my_pwd = "testpass"
    my_host = "LAPTOP-GG7823IL\SQLEXPRESS"
    my_db = "test"
    my_odbc_driver = "ODBC Driver 17 for SQL Server"

    connection_url = URL.create(
        "mssql+pyodbc",
        username=my_uid,
        #password=my_pwd,
        host=my_host,
        database=my_db,  # required; not an empty string
        query={
            "driver": my_odbc_driver ,
            "Trusted_Connection": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_engine(connection_url, fast_executemany=True)

    k = 0
    BAUD = 250000
    # wait for an available serial port
    while True:
        try:
            port = list(list_ports.comports())
            print(port)
            for p in port:
                print(p.device)
            connect_to = port[0].device
            ser = Serial(connect_to, BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
            print("Connected to: ", connect_to)
            continue_or_not = input("Press c to continue reading, q to quit: ")
            if continue_or_not == "q":
                break
            startup = battery_gauge(ser)
            time.sleep(0.1)
            startup.wait_for_connection()
            time.sleep(0.1)
            which_battery = startup.identify_device()
            

            if which_battery == "bq3060":
                print("bq3060")
                serial_number = startup.serial_number()
                time.sleep(0.1)
                print("test")
                with open('BQ3060_df.pkl', 'rb') as file:
                    print("1 ???")
                    # Load the dictionary from the file
                    data_df = pickle.load(file)
                with open('SBS_BQ3060.pkl', 'rb') as file:
                    print("2 ???")
                    # Load the dictionary from the file
                    data_SBS = pickle.load(file)
                print("check")
                current_battery = BQ3060(ser, data_df, data_SBS)
                time.sleep(0.1)
                
                
                current_battery.read_basic_SBS_new()
                print("Done reading SBS data for BQ3060...")
                with open('BQ3060_'+ serial_number + '_SBS.pkl', 'wb') as file:
                    pickle.dump(current_battery.data_SBS, file)
                print("Done saving SBS data for BQ3060 (pickle file, pandas dataframe)...")
                
                current_battery.data_SBS.to_sql('BQ3060_'+ serial_number + '_SBS', engine, if_exists='replace')
                print("Done sending SBS data for BQ3060 to server...")

                time.sleep(0.1)
                current_battery.read_all_dataflash_3060()
                print("Done reading dataflash for BQ3060...")
                # save dataframe to pickle file
                with open('BQ3060_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                    pickle.dump(current_battery.data_df, file)
                print("Done saving dataflash for BQ3060 (pickle file, pandas dataframe)...")
                
                current_battery.data_df.to_sql('BQ3060_' + serial_number + '_dataflash', engine, if_exists='replace')
                print("Done sending dataflash for BQ3060 to server...")

            if which_battery == "1936.1B-6":
                print("BQ4050")
                serial_number = startup.serial_number()
                time.sleep(0.1)
                with open('BQ4050_df.pkl', 'rb') as file:
                    # Load the dictionary from the file
                    data_df = pickle.load(file)
                with open('SBS_BQ4050.pkl', 'rb') as file:
                    # Load the dictionary from the file
                    data_SBS = pickle.load(file)
                current_battery= BQ4050(ser, data_df, data_SBS)
                time.sleep(0.1)
                current_battery.read_basic_SBS_new()
                print("Done reading SBS data for BQ4050...")
                with open('BQ4050_'+ serial_number + '_SBS.pkl', 'wb') as file:
                    pickle.dump(current_battery.data_SBS, file)
                print("Done saving SBS data for BQ4050 (pickle file, pandas dataframe)...")
                current_battery.data_SBS.to_sql('BQ4050_'+ serial_number + '_SBS', engine, if_exists='replace')
                print("Done sending SBS data for BQ4050 to server...")

                time.sleep(0.1)
                current_battery.read_all_dataflash_4050()
                print("Done reading dataflash for BQ4050...")
                # save dataframe to pickle file
                with open('BQ4050_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                    pickle.dump(current_battery.data_df, file)
                print("Done saving dataflash for BQ4050 (pickle file, pandas dataframe)...")
                current_battery.data_df.to_sql('BQ4050_' + serial_number + '_dataflash', engine, if_exists='replace')
                print("Done sending dataflash for BQ4050 to server...")
            if which_battery == "1737":
                serial_number = startup.serial_number()
                time.sleep(0.1)
                with open('BQ78350_df.pkl', 'rb') as file:
                    # Load the dictionary from the file
                    data_df = pickle.load(file)
                with open('SBS_BQ78350.pkl', 'rb') as file:
                    # Load the dictionary from the file
                    data_SBS = pickle.load(file)
                current_battery= BQ78350(ser, data_df, data_SBS)
                time.sleep(0.1)
                current_battery.read_basic_SBS_new()
                print("Done reading SBS data for BQ78350...")
                with open('BQ78350_'+ serial_number + '_SBS.pkl', 'wb') as file:
                    pickle.dump(current_battery.data_SBS, file)
                print("Done saving SBS data for BQ78350 (pickle file, pandas dataframe)...")
                current_battery.data_SBS.to_sql('BQ78350_'+ serial_number + '_SBS', engine, if_exists='replace')
                print("Done sending SBS data for BQ78350 to server...")

                time.sleep(0.1)
                current_battery.read_all_dataflash_78350()
                print("Done reading dataflash for BQ78350...")
                # save dataframe to pickle file
                with open('BQ78350_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                    pickle.dump(current_battery.data_df, file)
                print("Done saving dataflash for BQ78350 (pickle file, pandas dataframe)...")
                current_battery.data_df.to_sql('BQ78350_' + serial_number + '_dataflash', engine, if_exists='replace')
                print("Done sending dataflash for BQ78350 to server...")


        except:
            # print exception message
            print("Error: ", sys.exc_info()[0])
            # specify the error message
            print("Error: ", sys.exc_info()[1])
            if k % 10 == 0:
                print("Finding battery...")
            k+=1
            ser.close()
            time.sleep(0.1)
            pass
    



if len(sys.argv) > 1:
    if sys.argv[1] == "BQ4050":
        # Open a file in read binary mode
        with open('BQ4050_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('SBS_BQ4050.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery= BQ4050(data_df, data_SBS)
        time.sleep(0.1)
        if sys.argv[2] == "0":

            current_battery.read_basic_SBS_new()

            print(current_battery.data_SBS[:20])

            with open('BQ4050_SBS_saved.pkl', 'wb') as file:
                pickle.dump(current_battery.data_SBS, file)
            
            current_battery.data_SBS.to_sql('BQ4050_SBS', engine, if_exists='replace')
            
        elif sys.argv[2] == "1": 
            current_battery.read_all_dataflash_4050()
            # save dataframe to pickle file
            
            with open('saved_BQ4050.pkl', 'wb') as file:	
                pickle.dump(current_battery.data_df, file)
            
            current_battery.data_df.to_sql('BQ4050', engine, if_exists='replace')
            
    if sys.argv[1] == "BQ3060":
        with open('BQ3060_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('SBS_BQ3060.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery= BQ3060(data_df, data_SBS)
        time.sleep(0.1)
        if sys.argv[2] == "0":

            current_battery.read_basic_SBS_new()

            print(current_battery.data_SBS[:20])
            
            with open('BQ3060_SBS_saved.pkl', 'wb') as file:
                pickle.dump(current_battery.data_SBS, file)
            current_battery.data_SBS.to_sql('BQ3060_SBS', engine, if_exists='replace')

        elif sys.argv[2] == "1":
            current_battery.read_all_dataflash_3060()
            # save dataframe to pickle file
            with open('saved_BQ3060.pkl', 'wb') as file:	
                pickle.dump(current_battery.data_df, file)
            
            current_battery.data_df.to_sql('BQ3060', engine, if_exists='replace')
    
    if sys.argv[1] == "BQ78350":
        # TODO: add BQ78350
        pass
