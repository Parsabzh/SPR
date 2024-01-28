import pandas as pd
from engine.elastic_search import ElasticSearchManager
from chat import gpt


# list = [{
#     "keyword": "machine learning",
#     "expected_value": ["scikit-learn", "TensorFlow", "Keras", "PyTorch", "XGBoost"],
#     "suggested_value": ['tensorflow', 'pyspark', 'scikit-learn', 'PyOpenGL', 'torch', 'gensim', 'pygame']},
#     {"keyword": "data analysis",
#      "expected_value": ["Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn"],
#      "suggested_value":['pandas', 'gensim', 'scikit-learn', 'dash', 'redis', 'torch']
#      },
# {"keyword": "data analysis",
#      "expected_value": ["Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn"],
#      "suggested_value":['pandas', 'gensim', 'scikit-learn', 'dash', 'redis', 'torch']
#      },
#
# {"keyword": "",
#      "expected_value": ,
#      "suggested_value":
#      },
# ]


keywords = [
    "data analysis",
    "data science",
    "machine learning",
    "statistics",
    "predictive modeling",
    "data visualization",
    "neural networks",
    "deep learning",

    "web framework",
    "REST API",
    "web scraping",
    "web automation",

    "database",
    "SQL",
    "NoSQL",
    "ORM",

    "asynchronous",
    "asyncio",
    "concurrency",

    "testing",
    "automation",
    "DevOps",
    "continuous integration",
    "continuous delivery",

    "data visualization",
    "plotting",
    "charts",
    "dashboards",
    "BI tools",

    "mathematics",
    "linear algebra",
    "statistics",
    "physics",
    "chemistry",
    "engineering",

    "image processing",
    "object detection",
    "image classification",

    "NLP",
    "text analysis",
    "text classification",

    "GUI",
    "game development",
]

search = ElasticSearchManager()
client = gpt()
lst = []
package_name = []
package = {"keyword": "", "expected_value": "", "suggested_value": ""}
for keyword in keywords:

    response = search.search('package_index', keyword)
    for i in response["name"]:
        package_name.append(i)
    package["keyword"] = keyword
    package["suggested_value"] = package_name
    lst.append(package)

print(lst)
