from textblob import TextBlob
import pandas as pd

# Load LinkedIn Data
linkedin_file = 'linkedin_cleaned_data.json'
linkedin_df = pd.read_json(linkedin_file)

# Function to categorize Polarity into "Positive", "Negative", or "Neutral"
def get_polarity_label(polarity):
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Function to categorize Subjectivity into "Opinionated" or "Factual"
def get_subjectivity_label(subjectivity):
    return "Opinionated" if subjectivity > 0.5 else "Factual"

# Apply Analysis
linkedin_df['polarity'] = linkedin_df['text'].apply(lambda x: get_polarity_label(TextBlob(str(x)).polarity))
linkedin_df['subjectivity'] = linkedin_df['text'].apply(lambda x: get_subjectivity_label(TextBlob(str(x)).subjectivity))

# Save Results
output_csv = 'linkedin_polarity_subjectivity_analysis.csv'
output_json = 'linkedin_polarity_subjectivity_analysis.json'

linkedin_df.to_csv(output_csv, index=False, encoding='utf-8')
linkedin_df.to_json(output_json, orient='records', indent=4, force_ascii=False)

# Print Sample Output
print(linkedin_df[['text', 'polarity', 'subjectivity']].head())