from elasticsearch import Elasticsearch
import json


class ElasticSearchManager:
    def __init__(self):
        # Initialize Elasticsearch client

        self.es = Elasticsearch("https://localhost:9201", verify_certs=False,
                                http_auth=("elastic", "P2pGbll_CHBeo9n8jecF"))
        print(self.es.info())

        # Predefined mapping for Elasticsearch index
        self.mapping = {
            "settings": {
                "similarity": {
                    "default": {
                        "type": "BM25"
                    },
                    "dfi_similarity": {
                        "type": "DFI",
                        "independence_measure": "standardized"
                    },
                    "ib_similarity": {
                        "type": "IB",
                        "distribution": "ll",  # Log-logistic distribution
                        "lambda": "df",  # Document frequency
                        "normalization": {
                            "h1": 0.0,
                            "h2": 1.0,
                            "h3": 0.0
                        }
                    },
                    "lm_dirichlet_similarity": {
                        "type": "LMDirichlet",
                        "mu": 2000
                    }
                }
            },
            "mappings": {
                "properties": {
                    "softwareVersion": {
                        "type": "keyword"
                    },
                    "descriptionNAme": {
                        "type": "text"
                    },
                    "abstract": {
                        "type": "text"
                    },
                    "dateModified": {
                        "type": "date",
                        "format": "MMM d, yyyy"
                    },
                    "name": {
                        "type": "keyword"
                    },
                    "url": {
                        "type": "keyword"
                    },
                    "Quality Attribute": {
                        "type": "keyword"
                    },
                    "Resource utilization": {
                        "type": "keyword"
                    },
                    "Co-existence": {
                        "type": "keyword"
                    },
                    "Installability": {
                        "type": "keyword"
                    },
                    "Availability": {
                        "type": "keyword"
                    },
                    "Authenticity": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Appropriateness recognizability": {
                        "type": "keyword"
                    },
                    "User interface aesthetics": {
                        "type": "keyword"
                    },
                    "Time behaviour": {
                        "type": "keyword"
                    },
                    "Functional completeness": {
                        "type": "keyword"
                    },
                    "Modifiability": {
                        "type": "keyword"
                    },
                    "Learnability": {
                        "type": "keyword"
                    },
                    "Recoverability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Operability": {
                        "type": "keyword"
                    },
                    "Modularity": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Maturity": {
                        "type": "keyword"
                    },
                    "Functional correctness": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Confidentiality": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Functional appropriateness": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Adaptability": {
                        "type": "keyword"
                    },
                    "Capacity": {
                        "type": "keyword"
                    },
                    "Reusability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Fault tolerance": {
                        "type": "keyword"
                    },
                    "Integrity": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Accessibility": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "User error protection": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Testability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Analysability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Interoperability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Accountability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Non-repudiation": {
                        "type": "keyword",
                        "null_value": "unknown"
                    },
                    "Replaceability": {
                        "type": "keyword",
                        "null_value": "unknown"
                    }
                }
            }
        }

    def create_index(self, index_name):
        # Create an Elasticsearch index with the predefined mapping
        try:
            self.es.indices.create(index=index_name, body=self.mapping, ignore=400)
            print(f"Index '{index_name}' created.")
        except Exception as e:
            print(f"Error creating index: {e}")

    def index_documents(self, index_name, json_file_path):
        # Index documents from a JSON file into the specified Elasticsearch index
        try:
            with open(json_file_path) as json_file:
                packages = json.load(json_file)

            for package in packages:
                self.es.index(index=index_name, body=package)
            print("Indexing Complete")
        except Exception as e:
            print(f"Error indexing documents: {e}")

    def search(self, index_name, query):
        # Execute a search query against the specified Elasticsearch index
        try:
            query = {
                "query": {
                    "multi_match": {
                        "query": f"{query}",
                        "fields": ["name", "abstract", "about"]
                    }
                },

            }

            response = self.es.search(index=index_name, body=query)
            results = [hit['_source'] for hit in response['hits']['hits']]
            return results
        except Exception as e:
            print(f"Error executing search query: {e}")
            return None

    def delete(self):
        self.es.options(ignore_status=[400, 404]).indices.delete(index='package_index')

    def search_dfi(self, index_name, query):
        # Execute a search query against the specified Elasticsearch index
        try:
            dfi_query = {
                "query": {
                    "multi_match": {
                        "query": f"{query}",
                        "fields": ["name", "abstract^2", "about"],  # Boosting 'abstract' field
                        "type": "best_fields",
                        "tie_breaker": 0.3
                    }
                }
            }

            response = self.es.search(index=index_name, body=dfi_query)
            results = [hit['_source'] for hit in response['hits']['hits']]
            return results
        except Exception as e:
            print(f"Error executing search query: {e}")
            return None

    def search_ib(self, index_name, query):
        # Execute a search query against the specified Elasticsearch index
        try:
            ib_query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "abstract", "about"],
                        "similarity": "ib_similarity"
                    }
                }
            }

            response = self.es.search(index=index_name, body=ib_query)
            results = [hit['_source'] for hit in response['hits']['hits']]
            return results
        except Exception as e:
            print(f"Error executing search query: {e}")
            return None

    def lm_dirichlet(self, index_name, query):
        # Execute a search query against the specified Elasticsearch index
        try:
            lm_dirichlet_query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "abstract", "about"],
                        "similarity": "lm_dirichlet_similarity"
                    }
                }
            }

            response = self.es.search(index=index_name, body=lm_dirichlet_query)
            results = [hit['_source'] for hit in response['hits']['hits']]
            return results
        except Exception as e:
            print(f"Error executing search query: {e}")
            return None
# with open("output_package.json","r") as f:
#     data= json.load(f)
# se=ElasticSearchManager()
# se.delete()
# se.create_index("package_index")
# se.index_documents("package_index","output_package.json")
