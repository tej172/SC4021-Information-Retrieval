import requests
import time
# Solr URL
solr_url = "http://localhost:8983/solr/mycore/update/json/docs"

# Path to the JSON file
json_file = "data.json"

# Read the JSON data
with open(json_file, "r") as file:
    json_data = file.read()

# Send the JSON data to Solr
headers = {"Content-Type": "application/json"}
start_indexing = time.time() 
response = requests.post(solr_url, data=json_data, headers=headers)
indexing_duration = time.time() - start_indexing

print(f"Indexing Time: {indexing_duration:.3f} seconds")
# Check if the import was successful
if response.status_code == 200:
    print("JSON data imported successfully!")
else:
    print(f"Failed to import JSON data. Error: {response.text}")

# Commit the changes
commit_url = "http://localhost:8983/solr/mycore/update?commit=true"
commit_response = requests.get(commit_url)

if commit_response.status_code == 200:
    print("Changes committed successfully!")
else:
    print(f"Failed to commit changes. Error: {commit_response.text}")