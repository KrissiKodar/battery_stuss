import pandas as pd
import pickle

with open('saved_BQ3060.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
            

print(data_df.head(10))


# look at all rows that have CLASS = "SBS Configuration"
print(data_df.loc[data_df['CLASS'] == 'Charge Control'])