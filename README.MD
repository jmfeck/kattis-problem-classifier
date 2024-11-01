# Kattis Problem Classifier

Project presentation video: [YouTube Video Link](https://youtu.be/D6WK1fjt-XE)

This project aims to make competitive programming studies on Kattis more focused and efficient by categorizing problems based on solution types. Using web scraping and OpenAI’s API, this tool collects problem data, sends descriptions to ChatGPT for classification, and provides a consolidated Excel file that suggests a suitable algorithm type for each problem. This approach benefits anyone looking to streamline their practice in specific problem categories.

## Download the Results

For those interested in the problem classification results without diving into the code, the final Excel file with categorized Kattis problems is available **[here](https://github.com/jmfeck/kattis-problem-classifier/blob/main/data_outgoing/kattis_problems_combined.xlsx).**

This file includes an `Algorithm Type` column that reflects the classification provided by ChatGPT, indicating the type of solution approach recommended for each problem.

---

## Project Overview

The Kattis Problem Classifier project consists of several scripts designed to collect, process, and classify Kattis problems. Below is a breakdown of each script and its role in the pipeline:

### Script Workflow

1. **`kattis_problem_scraper.py`**  
   - **Purpose**: Scrapes Kattis to gather basic problem data, including titles, difficulty levels, and other metadata, for all available problems.
   - **Output**: Generates an initial Excel file containing the problem data.

2. **`kattis_problem_description_collector.py`**  
   - **Purpose**: Collects detailed descriptions for each problem by navigating to individual problem pages. This script runs in parallel to speed up the process.
   - **Output**: Adds a description column to the previously generated Excel, creating a new file.

3. **`kattis_problem_classifier.py`**  
   - **Purpose**: Uses OpenAI's API to classify each problem description by solution type, like dynamic programming or graph traversal. Processes are managed in 250-problem partitions to ensure efficient handling and recovery if needed.
   - **Output**: Generates multiple Excel files (one per partition) with an `algorithm_type` column reflecting the classification by ChatGPT.

4. **`kattis_problem_classifier_consolidation.py`**  
   - **Purpose**: Consolidates the multiple partitioned Excel files into a single, final Excel file.
   - **Output**: Creates `kattis_problems_combined.xlsx` in the `data_outgoing` folder, containing all Kattis problems with algorithm classifications.

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jmfeck/kattis-problem-classifier.git
   cd kattis-problem-classifier
   ```

2. **Set up the environment** (with Conda):
   ```bash
   conda env create -f environment.yml
   conda activate kattis-problems-classifier
   ```

3. **Configure OpenAI API**:
   Set your OpenAI API key in the appropriate script or environment variable:
   ```python
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

## Running the Pipeline

Follow this order to execute the scripts and obtain a final classification file:

1. **Scrape Kattis Problems**:
   ```bash
   python scripts/kattis_problem_scraper.py
   ```

2. **Collect Problem Descriptions**:
   ```bash
   python scripts/kattis_problem_description_collector.py
   ```

3. **Classify Problems by Solution Type**:
   ```bash
   python scripts/kattis_problem_classifier.py
   ```
   - Note: This script runs classifications in partitions of 250 problems each, resulting in multiple output files.

4. **Consolidate Results**:
   ```bash
   python scripts/kattis_problem_classifier_consolidation.py
   ```
   - Final consolidated file: `data_outgoing/kattis_problems_combined.xlsx`

---

## Additional Information

This project serves two main audiences:
- **Students and Developers**: Those who want to study Kattis problems by solution type can directly use the `kattis_problems_combined.xlsx` file as a reference.
- **Developers and Researchers**: Those interested in the methodology can examine the scripts to see how web scraping, parallel processing, and OpenAI API calls can be used to classify problems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
