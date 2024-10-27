# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 00:23:11 2024

@author: joaom
"""

import os
import pandas as pd
from openai import OpenAI

# Set up OpenAI client with API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY_KATTIS")
)

# Define file paths dynamically
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_path = os.path.dirname(script_dir)
data_incoming_path = os.path.join(project_path, 'data_incoming')
data_outgoing_path = os.path.join(project_path, 'data_outgoing')

# File paths for reading and writing
incoming_file_path = os.path.join(data_outgoing_path, 'kattis_problems_with_descriptions.xlsx')

# Classification function with batching
def classify_algorithm_type_batch(descriptions):
    prompt = "For each of the following problems, provide the primary tags only, such as Dynamic Programming, Graph Theory, etc.:\n\n"
    prompt += "\n\n".join([f"{i+1}. {desc}" for i, desc in enumerate(descriptions)])
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,  
        temperature=0.5
    )
    # Parse response, ensuring each description is tagged properly
    results = response.choices[0].message.content.strip().split("\n")
    return [line.split('. ', 1)[-1].strip() for line in results if '.' in line]


# Load data and determine unique partitions
df = pd.read_excel(incoming_file_path)
unique_partitions = df['Partition'].unique()

# Process each unique partition
for partition_number in unique_partitions:
    partition_df = df[df['Partition'] == partition_number].copy()
    
    batch_size = 5  
    algorithm_types = []
    
    for i in range(0, len(partition_df), batch_size):
        batch_descriptions = partition_df['Description'][i:i+batch_size].tolist()
        print(f"Processing batch {i//batch_size + 1}")
        
        for _ in range(2):  # Retry up to 2 times
            batch_results = classify_algorithm_type_batch(batch_descriptions)
            if len(batch_results) == len(batch_descriptions):
                break
            print("Retrying batch due to missing results...")
        else:
            # If still incomplete after retries, fill with 'Error'
            batch_results = batch_results + ["Error"] * (len(batch_descriptions) - len(batch_results))
        
        algorithm_types.extend(batch_results)
    
    # Add results to DataFrame and save
    partition_df['Algorithm Type'] = algorithm_types
    
    outgoing_file_path = os.path.join(data_outgoing_path, f'kattis_problems_with_classification_{partition_number}.xlsx')
    partition_df.to_excel(outgoing_file_path, index=False)

print(f"Algorithm types fetched and data saved to '{outgoing_file_path}'")