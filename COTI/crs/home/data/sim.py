from .engine.chat import gpt
import json
import ast
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import json
import pandas as pd
import os
from transformers import GPT2Tokenizer

client = gpt()
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
driver = webdriver.Chrome()

df = pd.DataFrame()
result = pd.DataFrame()


def extract_info_from_web(text):
    # Split the text into lines
    lines = text.split('\n')

    # Initialize an empty list to store the extracted data
    extracted_data = []

    # Process each line
    for line in lines:
        # Skip empty lines
        if not line.strip() or len(line) > 50:
            continue
        print(len(line))
        # Extract the keyword and its value
        parts = line.split('"')
        keyword = parts[1].strip()
        value = parts[3].strip()

        # Extract start and end indices
        index_parts = line.split('(')[-1].split(')')[0].split(',')
        start = int(index_parts[1].strip())
        end = int(index_parts[2].strip())

        # Append the formatted data to the list
        extracted_data.append((value, start, end, keyword))

    return extracted_data


def extract_info():
    global pagecontent
    packages = [
        'numpy'
    ]

    for package in packages:
        try:
            pip_url = f"https://pypi.org/project/{package}/"
            driver.get(pip_url)
            pagecontent = driver.find_element(By.TAG_NAME, 'body').text.replace('\n', '')
            # with open (f'{package}.txt', 'w') as f:
            #     f.write(pagecontent)
            #     f.close()
        except:
            pass

        text = f"""In this text \" {pagecontent}\". 
  create a NER training dataset from the text and this is the entity which is containing start and end position :
  \"LICENSE\", \"NAME\", \"VERSION\", \"REQUIRED\", \"OS\", \"RELEASED_DATE\", \"INSTALLED_URL\", \"DOMAIN\" """
        tokens = tokenizer.encode(text)
        if len(tokens) > 4000:
            continue
        respone = client.chat(text, max_tokens=1000)
        print(respone)
        lines = respone.split('\n')

        # Initialize an empty dictionary
        entities = {}
        # content=extract_info_from_web(respone)
        # print(content)

        # Iterate over each line
        for line in lines:
            # Split the line into key and value
            if ':' in line and len(line) < 100:
                key, value = line.split(':', 1)

                # Remove unnecessary characters
                key = key.strip(' -{"')
                value = value.strip(' },"')

                # Convert string representations of lists into actual lists
                if value.startswith('[') and value.endswith(']},'):
                    value = ast.literal_eval(value)
                    print(type(value))

                # Add to dictionary
                entities[key] = value
        print(entities)
        # with open(f'{package}.json', 'w') as file:
        #     json.dump(entities, file)
        return entities


def clean_data():
    folder_path = 'package_data/'

    # List of keys to keep
    keys_to_keep = ["LICENSE", "NAME", "VERSION", "REQUIRED", "OS", "RELEASED_DATE", "INSTALLED_URL", "DOMAIN"]

    # Iterate over all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            # Read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Remove keys not in keys_to_keep
            keys_to_remove = [key for key in data if key not in keys_to_keep]
            for key in keys_to_remove:
                del data[key]

            # Write the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Updated {filename}")

# clean_data()
# extract_info()
# result=pd.concat([result,df],axis=0)
# result.to_csv('data.csv')


# Sample text
# text = """
# 1. "VERSION": "9.5.0" (start: 9, end: 16)
# 2. "LICENSE": "MIT License" (start: 204, end: 217)
# 3. "NAME": "environs" (start: 229, end: 237)
# 4. "RELEASED_DATE": "Jan 30, 2022" (start: 227, end: 240)
# 5. "INSTALL_URL": "pip install environs" (start: 242, end: 263)
# 6. "DOMAIN": "configuration" (start: 254, end: 267)
# 7. "REQUIRED": "Python >=3.6" (start: 268, end: 281)
# 8. "OS": "OSI Approved :: MIT License" (start: 293, end: 320)
# """

# Extract keywords and their information from the text
# extracted_keywords = extract_info_from_web(text)
# print(extracted_keywords)
