import pandas as pd
import pickle

with open('saved_BQ4050.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
            

# print rows where Class is SBS configuration
print(data_df.loc[data_df['Class'] == 'Gas Gauging'])

