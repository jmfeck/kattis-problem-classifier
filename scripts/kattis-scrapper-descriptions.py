# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 22:45:06 2024
@author: joaom
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

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
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content of the problem statement (it's embedded in the page without a specific div class)
        main_content = soup.find('div', {'class': 'problembody'})
        if main_content:
            description_text = main_content.text.strip()
            return description_text
        else:
            return "No description found"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch: {e}"

# Step 1: Load the existing DataFrame from data_incoming
df = pd.read_excel(incoming_file_path)

# Step 2: Add a new column for the problem descriptions
print("Fetching problem descriptions...")
df['Description'] = df['Link'].apply(lambda link: fetch_description(link))

# Add a small delay to avoid overwhelming the server
time.sleep(1)

# Step 3: Save the updated DataFrame to Excel in data_outgoing
df.to_excel(outgoing_file_path, index=False)

# Print a success message
print(f"Problem descriptions fetched and data saved to '{outgoing_file_path}'")
