# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import requests

# Steps To Do:
# 1. Convert the JSON data into a DataFrame
# 2. Explore the data
# 3. Clean and manipulate the data
# 4. Analyze the data
# 5. Draw conclusions

# URL containing the book dataset in JSON format
url = "https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/books.json"

# Load JSON data into a Pandas DataFrame
df = pd.read_json(url, lines=True)

# Display basic information about the dataset
df.info()

# Function to clean the 'publishedDate' column by removing unnecessary characters
def clean_date(value):
    return re.sub(r"^{'.*: '|T00:00:.*'}|[|]", " ", value)

# Convert 'publishedDate' to string and apply the cleaning function
df['publishedDate'] = df['publishedDate'].astype(str).apply(clean_date)

# Clean 'authors' column by removing square brackets
df['authors'] = df['authors'].astype(str).str.replace(r"[\[\]]", "", regex=True)

# Display selected columns after initial cleaning
print(df[['_id', 'title', 'isbn', 'pageCount', 'publishedDate', 
          'thumbnailUrl', 'shortDescription', 'longDescription', 
          'status', 'authors', 'categories']])

# Check for missing values in the dataset
df.isnull().sum()

# Display dataset info after cleaning
df.info()

# Data Cleaning - Cleaning the 'isbn' column
# Removing any alphabetic characters appearing after numeric values
for i in range(len(df.isbn)):
    df.loc[i, 'isbn'] = re.sub(r'(?<=\d)[a-z]', '', str(df.loc[i, 'isbn']))
