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


import PySimpleGUI as sg


if __name__ == "__main__":

    BAUD = 250000
    frame_layout = [[sg.Multiline("", size=(80, 40), autoscroll=True,
        reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]]

    layout = [
        [sg.Frame("Output console", frame_layout)],
        [sg.Push(), sg.Button("Read battery")]
    ]
    window = sg.Window("Title", layout, finalize=True)

    connected = False

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Read battery":
            print('Reading battery...')
                try:
                    port = list(list_ports.comports())
                    print(port)
                    for p in port:
                        print(p.device)
                    connect_to = port[0].device
                    ser = Serial(connect_to, BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
                    print("Connected to: ", connect_to)
                    connected = True

                    # end serial connection
                    which_battery = startup.identify_device()

                    if which_battery == "bq3060":
                        print("bq3060")
                        serial_number = startup.serial_number()
                        time.sleep(0.1)
                        with open('BQ3060_df.pkl', 'rb') as file:
                            # Load the dictionary from the file
                            data_df = pickle.load(file)
                        with open('SBS_BQ3060.pkl', 'rb') as file:
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
                    
                    ser.close()
                except:
                    print("Already connected to: ", connect_to)


        

    window.close()