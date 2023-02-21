import pandas as pd
import pickle
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc
 
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


with open('saved_BQ3060.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)

#data_df.to_sql('BQ3060', engine, if_exists='replace')

with open('BQ3060_SBS.pkl', 'rb') as file:
            # Load the dataframe from the file
            data_df = pickle.load(file)

# move the index to a column called "Name"
data_df.reset_index(level=0, inplace=True)
# rename the index column to "Name"
data_df.rename(columns={'index': 'Name'}, inplace=True)
data_df.to_sql('BQ3060_SBS', engine, if_exists='replace')
#print(data_df[1:60])