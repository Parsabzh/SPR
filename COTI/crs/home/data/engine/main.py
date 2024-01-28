from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200") 

mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "version": {"type": "keyword"},
            "abstract": {"type": "text"},
            "description": {"type": "text"},
            "modified_date": {"type": "date"},
            "url": {"type": "keyword"}
        }
    }
}
es.indices.create(index="package_index", body=mapping)

query = {
    "query": {
        "multi_match": {
            "query": "your search term",
            "fields": ["name", "abstract", "description"]
        }
    }
}

# Execute the query
response = es.search(index="package_index", body=query)

# Process the results
for hit in response['hits']['hits']:
    print(hit['_source'])
