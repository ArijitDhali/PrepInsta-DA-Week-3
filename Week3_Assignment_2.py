import numpy as np
import pandas as pd

def standardize_item_names(data, column_name):
    name_mapping = {}                                                 # Create a dictionary to map variations to standardized names
    
    unique_names = data[column_name].unique()                         # Iterate through unique item names to identify variations
    for name in unique_names:
        standardized_name = name.lower().replace(' ', '')             # Generate a standardized name by converting to lowercase and removing spaces
        if standardized_name not in name_mapping:                     # Check if the standardized name is not already in the mapping
            name_mapping[standardized_name] = name                    # Map variations to the standardized name
            
    # Map variations to the standardized names in the DataFrame
    data['standardized_' + column_name] = data[column_name].apply(lambda x: name_mapping[x.lower().replace(' ', '')])
    return data


url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-3/main/Assignment2.tsv'
data=pd.read_csv(url,sep='\t',encoding='unicode_escape')      # sep='\t' helps to seperate the attributes 

data["choice_description"] = data["choice_description"].replace(np.nan, "[None]")     # Replace NULL value with "NONE"
data=data.drop_duplicates()                                   # Drop duplicates in data frame     

data["item_price"]=data["item_price"].str.lstrip("$")         # Strip '$' sign for ease transformation and analysis of data
data["item_price"] = data["item_price"].astype(float)         # Converting object data type to float data type

data["choice_description"]=data["choice_description"].str.replace('[','')       # Removing special characters like [,] from Choice_Descriptor column
data["choice_description"]=data["choice_description"].str.replace(']','')


data=standardize_item_names(data, 'item_name')                        # Passing the parameters to the function for standardizing the data
data=data.drop(columns='item_name')
column_to_shift2 = data.pop(data.columns[4])             # Remove column at index 4
data.insert(2, column_to_shift2.name, column_to_shift2)  # Insert the column at index 2


grouped_by_item = data.groupby('standardized_item_name')            # Grouping data by 'standardized_item_name'
mean_price_per_unit = {}                                            # Dictionary to store mean price per unit for inconsistent items
inconsistent_items_before = []                                      # Check consistency of price per unit for each item

for standardized_item_name, group in grouped_by_item:               
    price_per_unit = group['item_price'] / group['quantity']        # Calculate price per unit
    is_consistent = price_per_unit.round(2).nunique() == 1          # Check consistency by comparing price per unit across the item's data

    if not is_consistent:                                           # If price per unit is inconsistent, add the item to the list
        inconsistent_items_before.append(standardized_item_name)


for standardized_item_name, group in grouped_by_item:                         # Adjust inconsistent values
    price_per_unit = group['item_price'] / group['quantity']                  # Finding per unit value
    if not price_per_unit.round(2).nunique() == 1:                            
        mean_price_per_unit[standardized_item_name] = price_per_unit.mean()   # set the mean if it is not matching with the present value

for item in mean_price_per_unit:            # Replace inconsistent values with respective mean price per unit
    mask = data['standardized_item_name'] == item
    data.loc[mask, 'item_price'] = data.loc[mask, 'quantity'] * mean_price_per_unit[item] # If per unit doesn't match, replace with present value
data['item_price'] = data['item_price'].round(decimals=2)

split_choices = data["choice_description"].str.split(', ', expand=True)   # Splitting columns at ','

num_columns = split_choices.shape[1]                                 # Generate dynamic column names for the split columns
new_column_names = [f"choice_{i+1}" for i in range(num_columns)]
split_choices.columns = new_column_names                             # Assigning dynamic column names to the split columns
concatdata = pd.concat([data, split_choices], axis=1)                 # To concatenate data into new data frame
concatdata=concatdata.drop(columns=["choice_description"])  
column_to_shift = concatdata.pop(concatdata.columns[3])               # Remove column at index 3
concatdata.insert(13, column_to_shift.name, column_to_shift)          # Insert the column at index 13


data.to_csv('cleaned_chipotle.csv', index=False)                    # Method to convert .TSV to .CSV
chipotle_data = pd.read_csv('cleaned_chipotle.csv')                 # Verify its readability
print("Cleaned Data : ")
print(chipotle_data )
print("Cleaned Data with categorized item descriptions: ")
print(concatdata)
