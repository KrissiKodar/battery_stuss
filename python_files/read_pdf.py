from tabula.io import read_pdf


#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"


table =read_pdf(file1, pages=253,  multiple_tables=True, stream=True)

print(type(table[0]))

# turn the table[0] into a dictionary
print("\n\n\n")



# remove rows where the CLASS contains "Safety"
#table[0] = table[0][table[0]['CLASS'] != 'Safety']
# remove rows where the CLASS contains "2nd Level"
#table[0] = table[0][table[0]['CLASS'] != '2nd Level']
# remove row 0
#table[0] = table[0].drop(table[0].index[0])
# rename column Unnames: 0 to datatype
#table[0] = table[0].rename(columns={'Unnamed: 0': 'DATATYPE'})
#print(table[2])
# make a dictionary from the table
# like this table_dict ={NAME: [SUBCLASS.1, DATATYPE, UNIT]}
#table_dict = {}
#for index, row in table[0].iterrows():
#    table_dict[row['NAME']] = [row['SUBCLASS.1'], row['DATATYPE'], row['UNIT']]
# print the dictionary do it is easy to copy it to another file
#print(table_dict)
# remove all rows where the column class has nan
print(table[2])