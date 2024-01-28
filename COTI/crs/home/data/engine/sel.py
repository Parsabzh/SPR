# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import json
from text_sum import TextSummarizer
import pandas as pd
# Create a class to encapsulate the web scraping logic
class PyPiScraper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # Enable headless mode
        # chrome_options.add_argument('--disable-gpu')  # Disable GPU usage for headless mode
        # Setting a regular user-agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        # Disable Selenium flags
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize the driver
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(15)  # Set time in seconds for page load
        self.driver.set_script_timeout(15)     # Set time for asynchronous scripts to run

        self.driver.implicitly_wait(15)
        self.response=None
        self.text_summarizer=TextSummarizer()
        self.df=pd.read_csv('sentiment_modified.csv')

    def find_element_safe(self,action,arg):
        try:
            if action=='class':
                self.response=self.driver.find_element(By.CLASS_NAME, arg)
            elif action=='tag':
                self.response=self.driver.find_element(By.TAG_NAME, arg)
            elif action== 'xpath':
                self.response=self.driver.find_element(By.XPATH, arg)
            return self.response
        except Exception as e:
            print('error:',e)
            return None
    def find_elements_safe(self,action,arg):
        try:
            if action=='class':
                self.response=self.driver.find_elements(By.CLASS_NAME, arg)
            elif action=='tag':
                self.response=self.driver.find_elements(By.TAG_NAME, arg)
            elif action== 'xpath':
                self.response=self.driver.find_elements(By.XPATH, arg)
            return self.response
        except Exception as e:
            print('error:',e)
            return None
    

    def sentiment_analysis(self, name):
    # Replace NaN with None in the entire DataFrame
        self.df = self.df.fillna(value='null')
        
        # Convert the name to lowercase for case-insensitive comparison
        name = name.lower()

        # Iterate through each row in the DataFrame
        for index, row in self.df.iterrows():
            # Check if the first cell (converted to lowercase) matches the given name
            if name in str(row.iloc[0]).lower():
                # Create a dictionary with column names as keys and cell values as values
                return {self.df.columns[i]: row[i] for i in range(len(self.df.columns))}

        # Return 'null' if the name is not found in any row
        return "null"
    def scrape_package_info(self, url):
        # Navigate to the specified URL
        try: 
            self.driver.get(url)
        except Exception as e:
            print(f'Failed to load page at {url}',e)
            return None
        # Define a dictionary to store keyword-value pairs
        keyword_value_pairs = {}

        #Find elements on the page
        with open('pypi copy.json','r') as f:
            data=json.load(f)
        for item in data:
            if data[item]['xpath']!=None and data[item]['xpath']!='':
                if item=="license":
                    print(data[item]['xpath'])
                element=self.find_element_safe('xpath',data[item]['xpath'])
                if element==None:
                    keyword_value_pairs[item]=None
                    continue
                if data[item]['searchPattern']!=None and data[item]['searchPattern']!='':
                    if "split|[0]" in data[item]['searchPattern']:    
                        keyword_value_pairs[item]=element.text.split(' ')[0]
                    elif "split|[1]" in data[item]['searchPattern']:
                        z= element.text.split(' ')[1]
                        keyword_value_pairs[item]=element.text.split(' ')[1]
                    elif "loop" in data[item]['searchPattern']:
                        elements= element.find_elements(By.TAG_NAME, 'li')
                        element_list=[]
                        for element in elements:
                          element_list.append(element.text)
                else: 
                    if item=="about":
                        keyword_value_pairs[item]=self.text_summarizer.generate_summary(element.text)
                    else:
                        keyword_value_pairs[item]=element.text
            
        keyword_value_pairs['url']=url
        setiment= self.sentiment_analysis(keyword_value_pairs['name']) 
        if setiment is not None and setiment != "null":
          keyword_value_pairs.update(setiment)

        return keyword_value_pairs

    def scrape_package(self):

        python_packages = [
    "anaconda",
    "beautifulsoup",
    "django",
    "flask",
    "gensim",
    "kafka-python",
    "keras",
    "matplotlib",
    "mariadb",
    "mysql",
    "nltk",
    "numpy",
    "opencv-python",
    "pandas",
    "dash",
    'pymongo',
    'PyOpenGL',
    "pygame",
    "pyspark",
    "pillow",
    "torch",
    "redis",
    "requests",
    "scikit-learn",
    "scipy",
    "scrapy",
    "selenium",
    "db-sqlite3",
    "tensorflow"
]
        package_lst=[]

        for package in python_packages:
            package_url = f'https://pypi.org/project/{package}/'
            package_info = self.scrape_package_info (package_url)
            package_lst.append(package_info)
            print(package_info)
            print("-------------------------------------------------------------")
            print(package_lst)
        return package_lst


c=PyPiScraper()
# df= pd.read_csv('pypi copy.csv')
d=c.scrape_package()
json_string = json.dumps(d, indent=4)

# Write to file
with open('output_package.json', 'w') as file:
    file.write(json_string)

# Scrape the package information and print the result

