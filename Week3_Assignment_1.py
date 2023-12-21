import pandas as pd                 # We are not really calling pandas everytime
import numpy as np                  # Same case for numoy


# Splitting based on different separators for different locations
def split_location(row):
    location = row['Location']
    if ',' in location:                             # Split at ','
        parts = location.split(',')
        country = parts[0].strip()
        initials = parts[1].strip()
    elif ' ' in location:                           # Elif Split at ' '
        parts = location.split(' ')
        country = parts[0].strip()
        initials = parts[1].strip()
    else:                                            # Else split none
        country = location.strip()
        initials = None  # Or set initials as needed for cases with no separator

    return pd.Series({'Country': country, 'Initials': initials})        # Assigning each series with the values of particular row



url='https://raw.githubusercontent.com/ArijitDhali/PrepInsta-DA-Week-3/main/Assignment1.csv'      # To make this code available everywhere
df=pd.read_csv(url,encoding='unicode_escape')             # To ensure proper format of data frame

df=df.drop_duplicates()                                   # Dropping all the duplicate datas if present

df["Easy Apply"]=df["Easy Apply"].str.replace('-1','FALSE')         # Replacing -1 with False   
mapping = {'TRUE': True, 'FALSE': False}                            # Converting strings to boolean values
df = df.replace(-1, np.nan)                                         # Replacing the remaining -1 with NaN Value

df=df.dropna()                                                      # Drop all the rows where Null value is present

df[["Starting Salary","Ending Salary"]]=df["Salary"].str.split('-',1,expand=True)     # Splitting salary at '-'
df=df.drop(columns=["Salary"])                                                        # No more need of Salary column

df["Starting Salary"]=df["Starting Salary"].str.strip("$")          # Left Striping '$'
df["Ending Salary"]=df["Ending Salary"].str.strip("$")
df["Starting Salary"]=df["Starting Salary"].str.replace('k','000')  # Replacing 'k' with '000'
df["Ending Salary"]=df["Ending Salary"].str.replace('k','000')

df["Starting Salary"] = df["Starting Salary"].astype(int)           # Convert Starting salary to int data type
df["Ending Salary"] = df["Ending Salary"].astype(int)               # Convert Ending salary to int data type
df["Established"] = df["Established"].astype(int)                   # Convert Established to int data type
df["Age"] = df["Age"].astype(int)                                   # Convert Age to int data type
df['Easy Apply'] = df['Easy Apply'].map(mapping).fillna(False).astype(bool)   # Convert Easy Apply to int boolean type


# Apply the function to split 'Location' into 'Country' and 'Initials'
df[['Country', 'Initials']] = df.apply(split_location, axis=1)      # Assigning the splitted values of Location to new two columns
df=df.drop(columns=["Location"])                                    # No need of Location column anymore
df.reset_index(drop=True, inplace=True)                             # To restructure the index 
df.drop(columns=['Index'], inplace=True)
df
