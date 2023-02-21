from tabula.io import read_pdf
import pandas as pd
import pickle




# abandoned

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"

#file1 = "datasheets/BQ40z50_r2_tech_ref.pdf"
#table =read_pdf(file1, pages=253,  multiple_tables=True, stream=True)


""" file1 = "datasheets/BQ40z50_r2_tech_ref.pdf"
table =read_pdf(file1, pages="253-270",  multiple_tables=True)# stream=True) """

# read pages 253 to 270, but ignore the first 2 tables on page 253


file1 = "datasheets/BQ78350_r1_ref.pdf"
table =read_pdf(file1, pages="145-157",  multiple_tables=False)# stream=True)

#file1 = "datasheets/BQ3060_tech_ref.pdf"
# lets read from pages 178 to 185
#table =read_pdf(file1, pages="178-185",  multiple_tables=False)#, stream=True)

#print(type(table[0]))

#print(table[0])
#print(table[1])
#print(table[2])
#print(table[3])
#print(len(table))
#print(table[19])

# tables, table[2] to table[19] into one table
#for i in range(3,20):
#    table[2] = table[2].append(table[i], ignore_index=True)

#print(table[2])

# replace all instances of '\r' with ' ' in all columns
#for column in table[2]:
#    table[2][column] = table[2][column].str.replace('\r', ' ')
    
#print(table[2])


# remove from table all rows where the SUBCLASS\rID is SUBCLASS\rID
#table[0] = table[0].loc[table[0]['SUBCLASS\rID'] != 'SUBCLASS\rID']



    
# create empty column between "Type" and "Min Value" columns
#table[2].insert(5, "Measured Value", None)	






#print(table[2][40:50])
# convert Address where the numbers are strings "0x0000" to 32 bit integers
#table[2]["Address"] = table[2]["Address"].apply(lambda x: int(x, 16))	


# only print row where "Class" is "Settings" and Subclass is "Configuration"
#print(table[2].loc[(table[2]['Class'] == 'Settings') & (table[2]['Subclass'] == 'Configuration')])


# print all sublaclasses (one of each) to see how many different subclasses there are
#all_classes = table[2]["Class"].unique()
#all_subclasses = table[2]["Subclass"].unique()





""" import pickle
# Assuming your dictionary is called dict
# Open a file in write binary mode
with open('BQ4050_df.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(table[2], file) """

# print first value of column "Address"
#print(table[2]["Address"][0])


# put the data from each row of the table like this dict={ 'NAME': ['SUBCLASS', 'DATA\rTYPE', None, 'UNIT']}
# 'NAME','SUBCLASS','DATA\rTYPE','UNIT' are the column names

# in the all columns replace all instances of '\r' with ' '
for column in table[0]:
    table[0][column] = table[0][column].str.replace('\r', ' ')	

# in all column names replace all instances of '\r' with ' '
for column in table[0]:
    table[0] = table[0].rename(columns={column: column.replace('\r', ' ')})

# add empty column between "DATA TYPE" and "MIN VALUE" columns
table[0].insert(6, "Measured Value", None)		

print(table[0])

""" dict = {}
# Loop through the rows of the dataframe
for index, row in table[0].iterrows():
    # Get the name, subclass, data type and unit from the row
    name = row['NAME']
    subclass_ID = row['SUBCLASS\rID']
    data_type = row['DATA\rTYPE']
    offset = row['OFFSET']
    unit = row['UNIT']
    # Add the name as a key and the other values as a list to the dictionary
    dict[name] = [subclass_ID, data_type, None, offset, unit]
# Print the dictionary
print(dict) """


""" # print only part of dictionary where the value[0] is '0'

for key, value in dict.items():
    if value[0] == '0':
        print(key, value) """


# print all unique "SUBCLASS ID" values
print(table[0]["SUBCLASS ID"].unique())

#print row where "SUBCLASS ID" is "SUBCLASS ID"
print(table[0].loc[table[0]['SUBCLASS ID'] == 'SUBCLASS ID'])
# remove all rows where "SUBCLASS ID" is "SUBCLASS ID"
table[0] = table[0].loc[table[0]['SUBCLASS ID'] != 'SUBCLASS ID']	
print(table[0].loc[table[0]['SUBCLASS ID'] == 'SUBCLASS ID'])
#print(table[0].head(10))
# Import the pickle module
import pickle
# Assuming your dictionary is called dict
# Open a file in write binary mode
with open('BQ3060_df.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(table[0], file)