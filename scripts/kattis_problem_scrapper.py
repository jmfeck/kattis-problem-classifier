# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 22:45:06 2024
@author: joaom
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time

# Define file paths dynamically
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_path = os.path.dirname(script_dir)
data_incoming_path = os.path.join(project_path, 'data_incoming')
data_outgoing_path = os.path.join(project_path, 'data_outgoing')

outgoing_file_path = os.path.join(data_outgoing_path, 'kattis_problems.xlsx')

# Function to split 'Difficulty' into numeric score and level
def split_difficulty(value):
    # Check for a range of difficulty like '4.2 - 7.6Hard'
    match = re.match(r"([0-9.]+)\s*-\s*([0-9.]+)?([a-zA-Z]+)?", value)
    if match:
        # If a range is present
        min_difficulty = match.group(1)
        max_difficulty = match.group(2) if match.group(2) else None
        level = match.group(3) if match.group(3) else None
        return f"{min_difficulty} - {max_difficulty}" if max_difficulty else min_difficulty, level
    else:
        # Check for single value with difficulty level like '7.6Hard'
        match_single = re.match(r"([0-9.]+)([a-zA-Z]+)", value)
        if match_single:
            return match_single.groups()
    
    return value, None  # If no match, return the original value

list_of_tables = []
for i in range(1, 45):  # You can increase the range as needed for more pages
    
    # Step 1: Fetch the webpage content
    url = f"https://open.kattis.com/problems?page={i}"
    print(f"Fetching page {i}: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {i}: {e}")
        continue  # Skip to the next page
    
    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all tables with class 'table2'
    tables = soup.find_all('table', {'class': 'table2'})

    # Iterate through tables and find the one with the correct headers
    for table in tables:
        headers = [header.text.strip() for header in table.find_all('th')]
        if "Name" in headers:
            # Add an extra 'Link' column to the headers
            headers.insert(1, 'Link')
    
            # Extract the rows of the relevant table
            rows = []
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 0:
                    # Extract the problem name and link from the first cell
                    name_cell = cells[0]
                    problem_name = name_cell.text.strip()
                    problem_link = name_cell.find('a')['href'] if name_cell.find('a') else ''
    
                    # Get the remaining cell data
                    row_data = [problem_name, f"https://open.kattis.com{problem_link}"]
                    row_data += [cell.text.strip() for cell in cells[1:]]  # Append remaining columns
                    rows.append(row_data)
        
            # Convert the data into a DataFrame
            df = pd.DataFrame(rows, columns=headers)
            break  # Stop after finding the correct table
    list_of_tables.append(df)
    
    # Add a small delay to avoid overwhelming the server
    time.sleep(2)

# Step 3: Combine all DataFrames
combined_df = pd.concat(list_of_tables, ignore_index=True)

# Step 4: Handle the 'Difficulty' column if it exists
if 'Difficulty' in combined_df.columns:
    combined_df[['Difficulty Score', 'Difficulty Level']] = combined_df['Difficulty'].apply(lambda x: pd.Series(split_difficulty(x)))

# Step 5: Drop any empty columns or unwanted columns
columns_to_drop = ['Difficulty', '']  # Remove the Difficulty column after splitting and any unnamed columns
combined_df.drop(columns=[col for col in columns_to_drop if col in combined_df.columns], inplace=True)

# Step 6: Export the final DataFrame to Excel
combined_df.to_excel(outgoing_file_path, index=False)

# Print a success message
print(f"Data scraping and processing complete. Data saved to '{outgoing_file_path}'")
