import pandas as pd
import nltk
from textblob import TextBlob

# Load News Data
news_file = 'news_cleaned_data.json'  # Replace with your actual file
news_df = pd.read_json(news_file)


# Function to classify Polarity (-1 to 1) into categories
def get_polarity_label(text):
    polarity = TextBlob(str(text)).polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Function to classify Subjectivity (0 to 1) into categories
def get_subjectivity_label(text):
    subjectivity = TextBlob(str(text)).subjectivity
    return "Opinionated" if subjectivity > 0.5 else "Factual"

# Perform Sentiment, Polarity, and Subjectivity Analysis
if 'full_article' in news_df.columns:
    news_df['polarity'] = news_df['full_article'].apply(get_polarity_label)
    news_df['subjectivity'] = news_df['full_article'].apply(get_subjectivity_label)

# Save sentiment results
news_sentiment_csv = 'news_sentiment_analysis.csv'
news_sentiment_json = 'news_sentiment_analysis.json'
news_df.to_csv(news_sentiment_csv, index=False, encoding='utf-8')
news_df.to_json(news_sentiment_json, orient='records', indent=4, force_ascii=False)

# Print sentiment breakdown
print("News Sentiment Analysis Complete (Positive, Negative, Neutral)")
print("\nPolarity Breakdown:\n", news_df['polarity'].value_counts())
print("\nSubjectivity Breakdown:\n", news_df['subjectivity'].value_counts())