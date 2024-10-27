# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 00:23:11 2024

@author: joaom
"""

import pandas as pd
import os
import glob

# Define base paths
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
project_path = os.path.dirname(script_dir)
data_outgoing_path = os.path.join(project_path, 'data_outgoing')

# Find all Excel files in the folder that start with 'kattis_problems_with_classification_'
file_pattern = os.path.join(data_outgoing_path, 'kattis_problems_with_classification_*.xlsx')
file_paths = glob.glob(file_pattern)

# List to hold data from each file
data_frames = []

# Read each matching file and append its data to the list
for file_path in file_paths:
    df = pd.read_excel(file_path)
    data_frames.append(df)

# Concatenate all data frames into a single DataFrame
combined_df = pd.concat(data_frames, ignore_index=True)

# Save the combined DataFrame to a new Excel file
output_file_path = os.path.join(data_outgoing_path, 'kattis_problems_combined.xlsx')
combined_df.to_excel(output_file_path, index=False)

print(f"Combined data saved to '{output_file_path}'")
