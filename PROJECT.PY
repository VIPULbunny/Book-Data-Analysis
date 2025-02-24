# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import requests

# Fetch dataset from the given URL
url = "https://raw.githubusercontent.com/ozlerhakan/mongodb-json-files/master/datasets/books.json"

# Load the dataset from the JSON URL into a Pandas DataFrame
df = pd.read_json(url, lines=True)

# Function to clean and format the published date
def clean_date(value):
    return re.sub(r"^{'.*: '|-\d\d-\d\d+T00:00:.*'}|[|]", " ", value)

# Apply cleaning function to 'publishedDate' column
df['publishedDate'] = df['publishedDate'].astype(str).apply(clean_date)

# Clean 'authors' column by removing unnecessary brackets
df['authors'] = df['authors'].astype(str).str.replace(r"[\[\]]", "", regex=True)

# Check for missing values in the dataset
df.isnull().sum()

# Convert ISBN column to string type for further processing
df['isbn'] = df['isbn'].astype(str)

# Clean ISBN values by removing unwanted characters and letters
df['isbn'] = df['isbn'].str.replace(r'[a-z]- |[a-z]$', '', regex=True)

# Drop the 'isbn' column as it's not needed for analysis
df.drop('isbn', axis=1, inplace=True)

# Remove duplicate book titles from the dataset
df = df.drop_duplicates(subset=['title'])

# Assign unique numeric IDs to books
df['_id'] = np.arange(len(df))

# Replace missing values in 'pageCount' column with the mean page count
df['pageCount'].replace(0, df['pageCount'].mean().round(0), inplace=True)

# Rename 'publishedDate' column to 'PublishYear'
df.rename(columns={'publishedDate': 'PublishYear'}, inplace=True)

# Replace missing values in 'PublishYear' column with '0'
df['PublishYear'].replace('nan', '0', inplace=True)

# Convert 'PublishYear' column to integer type
df['PublishYear'] = df['PublishYear'].astype(int)

# Drop unnecessary columns that are not required for visualization
df.drop(['thumbnailUrl', 'shortDescription', 'longDescription', 'authors', '_id', 'categories'], axis=1, inplace=True)

# Replace 'MEAP' status with 'Unpublished' for consistency
df['status'].replace('MEAP', 'Unpublished', inplace=True)

# Visualize the count of books in each status category
plt.figure(figsize=(8, 5))
df['status'].value_counts().plot(kind='bar', color=['blue', 'green'])
plt.title('Book Status Distribution')
plt.xlabel('Status')
plt.ylabel('Count')
plt.grid()
plt.show()

# Plot a histogram of publication years
plt.figure(figsize=(8, 5))
df['PublishYear'].value_counts().plot(kind='hist', bins=5, color='purple', alpha=0.7)
plt.title('Publication Year Distribution')
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.grid()
plt.show()

# Identify top 10 books with the highest page count
top_books = df.sort_values('pageCount', ascending=False).head(10)

# Plot the top 10 books by page count
plt.figure(figsize=(10, 5))
plt.bar(top_books['title'], top_books['pageCount'], color='orange')
plt.xlabel('Book Title')
plt.ylabel('Page Count')
plt.title('Top 10 Books with the Highest Page Count')
plt.xticks(rotation=90)
plt.grid()
plt.show()
