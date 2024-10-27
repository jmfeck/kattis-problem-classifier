# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 22:45:06 2024
@author: joaom
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures

# Define file paths dynamically
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_path = os.path.dirname(script_dir)
data_incoming_path = os.path.join(project_path, 'data_incoming')
data_outgoing_path = os.path.join(project_path, 'data_outgoing')

# File paths for reading and writing
incoming_file_path = os.path.join(data_outgoing_path, 'kattis_problems.xlsx')
outgoing_file_path = os.path.join(data_outgoing_path, 'kattis_problems_with_descriptions.xlsx')

# Function to fetch the description of a problem from its link
def fetch_description(problem_link):
    try:
        response = requests.get(problem_link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', {'class': 'problembody'})
        description_text = main_content.text.strip() if main_content else "No description found"
        print(f"Fetched description for: {problem_link}")
        return description_text
    except requests.exceptions.RequestException as e:
        print(f"Link: {problem_link} | Error: {e}")
        return f"Failed to fetch: {e}"

# Load the existing DataFrame from data_incoming
df = pd.read_excel(incoming_file_path)

# Function to process each row in parallel
def process_row(index, link):
    description = fetch_description(link)
    return index, description

# Run fetching in parallel and store results
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start parallel processing and wait for completion
    results = [executor.submit(process_row, i, link) for i, link in enumerate(df['Link'])]
    for future in concurrent.futures.as_completed(results):
        index, description = future.result()
        df.at[index, 'Description'] = description

df['Description Length'] = df['Description'].apply(len)
df['Partition'] = (df.index // 250) + 1

# Save the updated DataFrame to Excel in data_outgoing
df.to_excel(outgoing_file_path, index=False)

# Print a success message
print(f"Problem descriptions fetched and data saved to '{outgoing_file_path}'")
