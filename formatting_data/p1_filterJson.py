import json
import os
from sentence_transformers import SentenceTransformer, util
import pickle

QUERY_EMBEDDING_FILE = "query_embedding.pkl"

# Load the existing data from the JSON file

'''REPLACE THE FILENAME WITH THE FILE YOU WANT TO FILTER'''
"""Back up the original file, before filtering"""
filename = 'OverallRecords.json'  # Replace with your actual file name
newFileName = 'fitlteredOverallRecords.json'  # Replace with your actual file name


def ComputeSimilarity(text):
        # Compute similarity between post and query
        post_embedding = model.encode(text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, post_embedding).item()
        return similarity

def CalculateReductionStats(original_data, filtered_data):
    original_count = len(original_data)
    filtered_count = len(filtered_data)
    reduction_count = original_count - filtered_count
    reduction_percentage = (reduction_count / original_count) * 100 if original_count > 0 else 0
    print(f"="*15)
    print(f"Original Data Count: {original_count}")
    print(f"Filtered Data Count: {filtered_count}")
    print(f"Data Reduced By: {reduction_count} items")
    print(f"Reduction Percentage: {reduction_percentage:.2f}%")
    print(f"="*15)

query = "Thoughts On AI Replacing Jobs"
# Load SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Check if query embedding is already saved
if os.path.exists(QUERY_EMBEDDING_FILE):
    with open(QUERY_EMBEDDING_FILE, "rb") as f:
        query_embedding = pickle.load(f)
    print("Loaded query embedding from file.")
else:
    query_embedding = model.encode(query, convert_to_tensor=True)
    with open(QUERY_EMBEDDING_FILE, "wb") as f:
        pickle.dump(query_embedding, f)
    print("Computed and saved query embedding.")

# Load the existing data from the JSON file
with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Assuming the data is a list of posts, and each post is a dictionary (like the `post_data` structure)
newData = []
for index, post in enumerate(data):
    print(index)
    # Add the subreddit attribute to each post (you can adjust as needed based on your structure)
    similarityText = ComputeSimilarity(post["text"]) 
    if similarityText> 0.5:
        newData.append(post)  

# Save the updated data back to the JSON file
with open(newFileName, 'w', encoding='utf-8') as file:
    json.dump(newData, file, indent=4)
print('Done')

# Calculate and display data reduction statistics
CalculateReductionStats(data, newData)

