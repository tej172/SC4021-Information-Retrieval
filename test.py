import pysolr
import subprocess
import requests
import time
import os

SOLR_PORT = 8983
current_dir = os.path.dirname(os.path.abspath(__file__))
solr_bin = os.path.join(current_dir, "./solr-9.8.0/bin/solr.cmd") # Change this to your actual Solr directory path

# Function to connect to Solr and index documents
def index_documents():
    # Connect to Solr core
    solr = pysolr.Solr('http://localhost:8983/solr/mycore', always_commit=True)

    # Index Documents
    documents = [
        {"id": "1", "title": "Solr Indexing", "content": "Solr uses Lucene for indexing"},
        {"id": "2", "title": "Jetty Server", "content": "Solr runs within a Jetty servlet container"},
    ]

    solr.add(documents)
    print("Documents indexed successfully!")

# Function to search in Solr
def search_documents():
    # Connect to Solr core
    solr = pysolr.Solr('http://localhost:8983/solr/mycore')

    # Search in Solr
    results = solr.search("title:Solr")

    for result in results:
        print(f"ID: {result['id']}, Title: {result['title']}, Content: {result['content']}")


def delete():
    # Connect to Solr core
    solr = pysolr.Solr('http://localhost:8983/solr/mycore')

    solr.delete(id="1")
    solr.delete(q="title:Jetty")
    print("Documents deleted successfully!")

def adv():
    # Advanced Queries
    # You can perform more complex searches using filters and faceting:
    # Connect to Solr core
    solr = pysolr.Solr('http://localhost:8983/solr/mycore')

    results = solr.search("content:Lucene", **{"rows": 10, "fl": "id,title"})

    for result in results:
        print(result)

# Main script logic
if __name__ == "__main__":

    # Index documents
    index_documents()

    # Search for documents
    search_documents()
