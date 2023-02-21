import pandas as pd
import pickle

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'localhost\SQLEXPRESS' 
# database = 'master' 
# username = 'krissi' 
# password = 'testpass' 
""" conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost\SQLEXPRESS;'
                      'Database=test;'
                      'Trusted_Connection=yes;') """
#cursor = conn.cursor()


#LAPTOP-GG7823IL\SQLEXPRESS
# user = LAPTOP-GG7823IL\dadas
# password = '1234'
# server = 'LAPTOP-GG7823IL\SQLEXPRESS'

my_uid = "LAPTOP-GG7823IL\dadas"
#my_pwd = "testpass"
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


print(connection_url)

engine = create_engine(connection_url, fast_executemany=True)

insp = sqlalchemy.inspect(engine)
db_list = insp.get_schema_names()
print(db_list)


#engine = sqlalchemy.create_engine("mssql+pyodbc://krissi:testpass@LAPTOP-GG7823IL\SQLEXPRESS;master;trusted_connection=true")

#print(engine)

with open('saved_BQ4050.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)




#engine = sqlalchemy.create_engine("mssql+pyodbc://LAPTOP-GG7823IL\SQLEXPRESS/BQ40z50?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes")


#data_df.to_sql('BQ4050', engine, if_exists='replace')

# print all Class values
#print(data_df['Class'].unique())
""" ['Calibration' 'Settings' 'Advanced Charge Algorithm' 'Power'
 'LED Support' 'System Data' 'SBS Configuration' 'Lifetimes' 'Protections'
 'Permanent Fail' 'PF Status' 'Black Box' 'Gas Gauging' 'Ra Table'] """
# print rows where Class is Power
print(data_df.loc[(data_df['Class'] == 'Calibration') & (data_df['Subclass'] == 'Internal Temp Model')])

with open('BQ4050_SBS.pkl', 'rb') as file:
            # Load the dataframe from the file
            data_df = pickle.load(file)

""" # move the index to a column called "Name"
data_df.reset_index(level=0, inplace=True)
# rename the index column to "Name"
data_df.rename(columns={'index': 'Name'}, inplace=True) """

print(data_df[:])


#data_df.to_sql('BQ4050_SBS', engine, if_exists='replace')