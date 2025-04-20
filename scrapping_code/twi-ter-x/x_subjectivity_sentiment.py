import pandas as pd
from textblob import TextBlob

# Load the crawled tweet data
file_path = "crawled_tweets.csv"  # Update the file path
df = pd.read_csv(file_path)

# Function to detect subjectivity
def detect_subjectivity(text):
    analysis = TextBlob(str(text))
    return "Opinionated" if analysis.sentiment.subjectivity > 0.5 else "Neutral"

# Function to detect polarity (positive, negative, or neutral)
def detect_polarity(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Apply subjectivity and polarity detection
df["Subjectivity"] = df["Text"].apply(detect_subjectivity)


df["Sentiment"] = df["Text"].apply(detect_polarity)

# Save the updated file with subjectivity and sentiment
output_path = "crawled_tweets_with_subjectivity_sentiment.csv"
df.to_csv(output_path, index=False)

print(f"Subjectivity and sentiment analysis completed. New file saved as {output_path}")
