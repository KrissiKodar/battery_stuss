from tabula.io import read_pdf
import pickle

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"

#file1 = "datasheets/BQ40z50_r2_tech_ref.pdf"
#table =read_pdf(file1, pages=253,  multiple_tables=True, stream=True)

file1 = "datasheets/BQ3060_tech_ref.pdf"
#table =read_pdf(file1, pages=178,  multiple_tables=True, stream=True)


# lets read from pages 178 to 185
table =read_pdf(file1, pages="178-185",  multiple_tables=False)#, stream=True)

print(type(table[0]))

# print dimensions of the table
print(table[0].shape)

# turn the table[0] into a dictionary
print("\n\n\n")
print(table)
print(type(table))


# remove from table all rows where the SUBCLASS\rID is SUBCLASS\rID
table[0] = table[0].loc[table[0]['SUBCLASS\rID'] != 'SUBCLASS\rID']


# 


# put the data from each row of the table like this dict={ 'NAME': ['SUBCLASS', 'DATA\rTYPE', None, 'UNIT']}
# 'NAME','SUBCLASS','DATA\rTYPE','UNIT' are the column names

dict = {}
# Loop through the rows of the dataframe
for index, row in table[0].iterrows():
  # Get the name, subclass, data type and unit from the row
  name = row['NAME']
  subclass = row['SUBCLASS']
  data_type = row['DATA\rTYPE']
  unit = row['UNIT']
  # Add the name as a key and the other values as a list to the dictionary
  dict[name] = [subclass, data_type, None, unit]
# Print the dictionary
print(dict)

""" # Import the pickle module
import pickle
# Assuming your dictionary is called dict
# Open a file in write binary mode
with open('data_dict_3060.pkl', 'wb') as file:
  # Dump the dictionary to the file
  pickle.dump(dict, file) """