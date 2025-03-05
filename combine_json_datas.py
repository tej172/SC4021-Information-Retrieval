import os
import json

# Define the folder containing the JSON files
folder_path = r"C:\Users\tegti\OneDrive\Documents\MERN\School\SC4021-InfoRet\SC4021-Information-Retrieval\data\separate_data"
output_file = r"C:\Users\tegti\OneDrive\Documents\MERN\School\SC4021-InfoRet\SC4021-Information-Retrieval\data\combined_data\combined.json"

# Aggregate data from all JSON files
all_data = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.extend(data)  # Add all entries from the file to the main list

# Write the output to a single JSON file
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(all_data, out_file, indent=2, ensure_ascii=False)

print(f"Combined JSON files saved to {output_file}")