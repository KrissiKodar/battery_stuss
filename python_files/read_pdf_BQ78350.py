from tabula.io import read_pdf
import pandas as pd
import pickle

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"



file1 = "datasheets/BQ78350_r1_ref.pdf"
table =read_pdf(file1, pages="145-157",  multiple_tables=True)



#print(type(table[0]))
#print(len(table))
#print(table[1])
#print(table[0])
#print(table[1])
# combine tables table[0] to table[-1] into one table
for i in range(2,len(table)):
    table[1] = table[1].append(table[i], ignore_index=True)

#print(table[1])

#remove all instances of '\r', '\t' and '\n' from all columns
for column in table[1]:
    table[1][column] = table[1][column].str.replace('\r', ' ')
    table[1][column] = table[1][column].str.replace('\t', ' ')
    table[1][column] = table[1][column].str.replace('\n', ' ')

#print(table[1])


# add column "Measured Value" to table[1] and fill it with None
# between columns "Type" and "Min Value"
table[1].insert(5, "Measured Value", None)

# convert Address where the numbers are strings "0x0000" to 32 bit integers
table[1]["Address"] = table[1]["Address"].apply(lambda x: int(x, 16))



print(table[1][20:40])
with open('BQ78350_df.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(table[1], file)