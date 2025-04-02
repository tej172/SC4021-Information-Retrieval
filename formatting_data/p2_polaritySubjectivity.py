import json
from textblob import TextBlob

# Load the existing data from the JSON file
'''REPLACE THE FILENAME WITH THE FILE YOU WANT TO FILTER'''
filename = f'filteredOverallRecords.json'  # Replace with your actual file name

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        sentiment = "positive"
    elif analysis.sentiment.polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    if analysis.sentiment.subjectivity > 0.5:    
        subjectivity = "opinionated"  
    else:
        subjectivity = "neutral"
    # "positive" if analysis.sentiment.polarity > 0 "negative" elif analysis.sentiment.polarity > 0 else "neutral"
    return sentiment, subjectivity


with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Assuming the data is a list of posts, and each post is a dictionary (like the `post_data` structure)
for index, post in enumerate(data): 
    print(index)
    # Add the subreddit attribute to each post (you can adjust as needed based on your structure)
    post["polarity"], post["subjectivity"] = get_sentiment(post["text"])
  

# Save the updated data back to the JSON file
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
print('Done')
