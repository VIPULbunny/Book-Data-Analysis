# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import requests

# URL containing the book dataset in JSON format
url = "https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/books.json"

# Optional request check (commented out)
# req = requests.get(url)
# print(req)

# Load JSON data into a DataFrame
df = pd.read_json(url, lines=True)

# Display DataFrame info and sample data for initial inspection
# print(df.info())
# print(df['_id'][398])  # Check the last ID
# print(df['categories'][])  # Incorrect syntax - needs fixing if required

# Function to clean 'publishedDate' by removing unwanted characters
def clean_date(value):
    # Remove pattern like {'date': 'YYYY-MM-DD'} and unwanted characters
    return re.sub(r"^{'.*: '|T00:00:.*'}|[|]", " ", value)

# Apply the cleaning function to the 'publishedDate' column
df['publishedDate'] = df['publishedDate'].astype(str).apply(clean_date)

# Clean 'authors' column by removing square brackets
df['authors'] = df['authors'].astype(str).str.replace(r"[\[\]]", "", regex=True)

# Display selected columns after cleaning
print(df[['_id', 'title', 'isbn', 'pageCount', 'publishedDate',
          'thumbnailUrl', 'shortDescription', 'longDescription',
          'status', 'authors', 'categories']])

# Check for missing values in the dataset
df.isnull().sum()

# Display DataFrame structure and data types
df.info()

# Data Cleaning: Clean the 'isbn' column

# Convert 'isbn' column to string for regex operations
df['isbn'] = df['isbn'].astype(str)

# Apply regex pattern to remove unwanted letters or symbols in ISBN
df['isbn'] = df['isbn'].str.replace(r'[a-z]-|[a-z]$', '', regex=True)  # Removes patterns like 'a-e'

# Check the last few cleaned ISBN values
df.isbn.tail()

# Display the full DataFrame
df

# Check rows where ISBN is missing
df[df.isbn.isna() == True]

# Print ISBN values in a specific range
print(df['isbn'][19:25])

# Drop the 'isbn' column if not required
df.drop('isbn', axis=1, inplace=True)

# Display the DataFrame after dropping the 'isbn' column
print(df)

# Get unique book titles
df.title.unique()

# Check for duplicated titles (returns a Series of True/False)
df.title.duplicated()

# Display rows with duplicated titles
df[df.title.duplicated()]

# Filter DataFrame to find details about a specific book title
df[df['title'] == "Jaguar Development with PowerBuilder 7"]
