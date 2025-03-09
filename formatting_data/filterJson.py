import json
import os
from sentence_transformers import SentenceTransformer, util
import pickle

QUERY_EMBEDDING_FILE = "query_embedding.pkl"

# Load the existing data from the JSON file
'''REPLACE THE FILENAME WITH THE FILE YOU WANT TO FILTER'''
filename = 'OverallRecords.json'  # Replace with your actual file name
newFileName = 'fitlteredOverallRecords.json'  # Replace with your actual file name


def ComputeSimilarity(text):
        # Compute similarity between post and query
        post_embedding = model.encode(text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, post_embedding).item()
        return similarity

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

