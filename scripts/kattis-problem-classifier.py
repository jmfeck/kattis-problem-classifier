# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 00:23:11 2024

@author: joaom
"""

import os
import openai
import pandas as pd

# Define file paths dynamically
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_path = os.path.dirname(script_dir)
data_incoming_path = os.path.join(project_path, 'data_incoming')
data_outgoing_path = os.path.join(project_path, 'data_outgoing')

# File paths for reading and writing
incoming_file_path = os.path.join(data_outgoing_path, 'kattis_problems_with_descriptions.xlsx')
outgoing_file_path = os.path.join(data_outgoing_path, 'kattis_problems_with_solutions.xlsx')

# Set up your OpenAI API key
openai.api_key = "api-key"

# Function to classify the problem description using OpenAI's new API
def classify_with_openai(description):
    try:
        # Send a request to OpenAI's ChatGPT model using the newer API interface
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use gpt-3.5-turbo as well
            messages=[
                {"role": "system", "content": "You are a helpful assistant who classifies algorithmic problems."},
                {"role": "user", "content": f"Classify the following problem description into a probable algorithmic solution (e.g., Dynamic Programming, Graph Theory, Greedy Algorithm, etc.):\n\n{description}"}
            ],
            max_tokens=100,
            temperature=0.5
        )
        # Extract the assistant's response from the API response
        probable_solution = response['choices'][0]['message']['content'].strip()
        return probable_solution
    except Exception as e:
        return f"API Error: {e}"

# Step 1: Load the existing DataFrame from the Excel file
df = pd.read_excel(incoming_file_path)

# Step 2: Add a new column for the probable solutions
print("Fetching probable solutions from OpenAI...")

df['Probable Solution'] = df['Description'].apply(classify_with_openai)

# Step 3: Save the updated DataFrame to Excel in data_outgoing
df.to_excel(outgoing_file_path, index=False)

# Print a success message
print(f"Problem solutions fetched and data saved to '{outgoing_file_path}'")
