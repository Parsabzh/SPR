import nltk
import re
import json
from nltk.tokenize import word_tokenize

# Sample text for demonstration purposes
text = "This software is released under the MIT LICENSE. The NAME is ExampleApp. VERSION 1.2.3 is REQUIRED. Compatible with Windows OS. RELEASED_DATE is 2021-01-01. Find it at INSTALLED_URL: https://www.example.com. It's used in the DOMAIN of data processing."

# Tokenize the text
tokens = word_tokenize(text)

# Define patterns for each entity
patterns = {
    "LICENSE": "MIT|GPL|Apache",  # Add more license types as needed
    "NAME": r"\bNAME is (\w+)",
    "VERSION": r"VERSION (\d+\.\d+\.\d+)",
    "REQUIRED": "REQUIRED",
    "OS": r"Windows|MacOS|Linux|OS Independent",
    "RELEASED_DATE": r"\d{4}-\d{2}-\d{2}",
    "INSTALLED_URL": r"https?://\S+",
    "DOMAIN": r"DOMAIN of (\w+)"
}

# Function to extract entities based on patterns
def extract_entities(text, patterns):
    entities = {}
    for entity, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            entities[entity] = match.group()
    return entities

# Extract entities
extracted_entities = extract_entities(text, patterns)

# Convert to JSON
json_output = json.dumps(extracted_entities, indent=4)
print(json_output)
