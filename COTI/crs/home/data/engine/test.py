from chat import gpt
from elastic_search import ElasticSearchManager
import json

client = gpt()

keywords = [
    "Data Science", "Web Scraping", "Web Framework", "Natural Language Processing",
    "Stream Processing", "Deep Learning", "Database", "Data Visualization",
    "NoSQL Database", "Numerical Computing", "Computer Vision", "Graphics Rendering",
    "Data Analysis", "Interactive Dashboards", "Game Development", "Big Data Processing",
    "Image Processing", "In-memory Database", "HTTP Requests", "Machine Learning",
    "Scientific Computing", "Web Crawling", "Web Automation", "API Development",
    "Object-Relational Mapping", "Asynchronous Programming", "Data Mining",
    "Statistical Analysis", "Data Manipulation", "Data Cleaning", "Text Analysis",
    "Parallel Computing", "Distributed Computing", "Data Storage", "Query Language",
    "Plotting Library", "Visualization Tools", "Real-time Data", "Time Series Analysis",
    "Neural Networks", "Artificial Intelligence", "Cluster Computing", "Memory Management",
    "Performance Optimization", "Web Testing", "Browser Automation", "Data Integration",
    "Data Aggregation", "Data Wrangling", "File Handling"
]
search = ElasticSearchManager()
client = gpt()
lst = []
# package_name = []
# package = {"keyword": "", "expected_value": "", "suggested_value": ""}


def bm25():
    for keyword in keywords:
        response = search.search('package_index', keyword)
        package_name = [i["name"] for i in response]

        package = {
            "keyword": keyword,
            "suggested_value": package_name,
            "suggested_value": []}
        lst.append(package)

    with open("test_bm25.json", 'w') as file:
        json.dump(lst, file)

    print(lst)

