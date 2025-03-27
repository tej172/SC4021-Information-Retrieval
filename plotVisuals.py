
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for Flask
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
import base64
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import plotly
import plotly.graph_objs as go
import json
import seaborn as sns
import pandas as pd
from PIL import Image

# Ensure that NLTK data is downloaded
#nltk.download('punkt_tab')
#nltk.download('stopwords')
#nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('stopwords')

'''
[{'id': '1', 'text': ['If ai speeds up work or even regularly does a single task, that displaces jobs.\n\nReduced workload -> reduced headcount'], 
  'time': [1718039224.0], 'popularity': [463], 
  'source': ['Reddit'], 
  'polarity': ['negative'], 
  'subjectivity': ['neutral'],
  'category': ['Technology & IT', 'Consumer Goods & Services', 'Non-Profit & Social Services', 'Manufacturing & Engineering', 'Human Resources & Talent Management'], 
  'date': ['2024-06-10'], '_version_': 1826306439897939968, '_root_': '1'},.....]
'''
def generate_placeholder_image():
    """Creates a placeholder image with a message and returns its base64 string."""
    plt.figure(figsize=(10, 5))
    plt.text(0.5, 0.5, "No data available", fontsize=20, ha='center', va='center', color='gray')
    plt.axis("off")

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    return Image.open(img)

def wordCloud(results):
    
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image

    text = ''
    for post in results:
        text += post['text'][0]

    # Tokenize and filter stop words
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]

    # Generate word frequencies
    word_freq = nltk.FreqDist(filtered_tokens)

    # Create the word cloud
    wordcloud = WordCloud(width=800, height=300, background_color='white', colormap='brg').generate_from_frequencies(word_freq)

    # Create an image to save
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Overall Word Cloud")
    # Save the image to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # Higher DPI for quality
    img.seek(0)

    # Encode the image to base64 to pass it to HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url  # Return base64 string of the word cloud image



def word_cloud_of_ai_discussions(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(results)

    # Explode the lists in the 'text' and 'polarity' columns
    df_expanded = df.explode('text')  # Exploding the 'text' column to separate entries if it's a list
    df_expanded['polarity'] = df_expanded['polarity'].explode()  # Exploding 'polarity'

    # Concatenate the text from positive and negative sentiments
    positive_text = " ".join(df_expanded[df_expanded["polarity"] == "positive"]["text"])
    negative_text = " ".join(df_expanded[df_expanded["polarity"] == "negative"]["text"])


    if not positive_text:  # Handle no positive text 
        wordcloud_positive = generate_placeholder_image()  # Return the placeholder image
    else:
        wordcloud_positive = WordCloud(width=400, height=200,background_color="white", colormap="Greens").generate(positive_text)

    if not negative_text:  # ✅ Handle no negative text
        wordcloud_negative = generate_placeholder_image()  # Return the placeholder image
    # Generate word clouds for positive and negative texts
    else:
        wordcloud_negative = WordCloud(width=400, height=200,background_color="white", colormap="Reds").generate(negative_text)

    # Create a figure to display both word clouds side by side
    plt.figure(figsize=(10, 5))

    # Plot the positive word cloud
    plt.subplot(1, 2, 1)
    plt.imshow(wordcloud_positive, interpolation='bilinear')
    plt.axis("off")
    plt.title("Positive Sentiment Word Cloud")

    # Plot the negative word cloud
    plt.subplot(1, 2, 2)
    plt.imshow(wordcloud_negative, interpolation='bilinear')
    plt.axis("off")
    plt.title("Negative Sentiment Word Cloud")

    # Save the image to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # High quality image
    plt.close()
    img.seek(0)

    # Encode the image to base64 to pass it to HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url  # Return base64 string of the word cloud image

def polarityDistribution(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image
    
    # Count the number of posts for each polarity
    positive = negative = neutral = 0
    for post in results:
        if post['polarity'][0] == 'positive':
            positive += 1 
        elif post['polarity'][0] == 'negative':
            negative += 1
        else:  # post['polarity'][0] == 'neutral'
            neutral += 1

    data = {
        'positive': positive,
        'neutral': neutral,
        'negative': negative
    }

    # Filter out categories with 0 count
    data = {key: value for key, value in data.items() if value > 0}

    # If all categories have 0 counts, return a default empty plot
    if not data:
        return None  # Or you could return a default base64 image of an empty pie chart

    categories = list(data.keys())
    values = list(data.values())

    # Define custom colors for the pie chart (ensure color length matches remaining categories)
    color_mapping = {'positive': 'green', 'neutral': 'gray', 'negative': 'red'}
    colors = [color_mapping[category] for category in categories]

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        values, 
        labels=categories, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,  # Apply filtered color list
        textprops={'color': 'black', 'fontsize': 14}
    )

    # Display percentage and value inside the chart
    for autotext in autotexts:
        autotext.set_fontsize(14)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Title of the plot
    plt.title("Polarity Composition", fontsize=16)

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # High quality image
    plt.close()
    img.seek(0)

    # Encode the image to base64 to pass it to HTML
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url  # Return base64 string of the pie chart image

#NEW ONES 
'''
[{'id': '1', 
 'text': ['If ai speeds up work or even regularly does a single task, that displaces jobs.\n\nReduced workload -> reduced headcount'], 
 'time': [1718039224.0], 'popularity': [463], 'source': ['Reddit'], 'polarity': ['negative'], 
 'subjectivity': ['neutral'],
 'category': ['Technology & IT', 'Consumer Goods & Services', 'Non-Profit & Social Services', 'Manufacturing & Engineering', 'Human Resources & Talent Management'], 
 'date': ['10-06-2024'], 
 '_version_': 1827037896758001664, 
 '_root_': '1'},,.....]
'''


def sentiment_distribution_by_industry(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(results)

    # Explode the 'category' field into multiple rows
    df_expanded = df.explode('category')

    # Extract polarity (assuming it's a list, so taking the first element if it's a list)
    df_expanded['polarity'] = df_expanded['polarity'].apply(lambda x: x[0] if isinstance(x, list) else x)

    # Plotting the sentiment distribution by industry
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df_expanded, x="category", hue="polarity", 
                  palette={"positive": "green", "neutral": "yellow", "negative": "red"})
    plt.xticks(rotation=45, ha="right")
    plt.title("Sentiment Distribution by Industry")
    plt.xlabel("Industry")
    plt.ylabel("Count of Opinions")
    plt.legend(title="Sentiment")

    # Save the plot to a BytesIO object and return it as a base64 encoded string
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')


def sentiment_over_time_with_milestones(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(results)

    # Extract the date (handle it if it's a list)
    df['date'] = df['date'].apply(lambda x: x[0] if isinstance(x, list) else x)
    
    # Extracting polarity (since it's a list, we assume there's only one value per row)
    df['polarity'] = df['polarity'].apply(lambda x: x[0] if isinstance(x, list) else x)
    
    # Grouping by date and polarity to count sentiments
    df_time_sentiment = df.groupby(['date', 'polarity']).size().unstack(fill_value=0)
    
    # Adding missing sentiment columns if they're not in the dataset
    for sentiment in ["positive", "neutral", "negative"]:
        if sentiment not in df_time_sentiment.columns:
            df_time_sentiment[sentiment] = 0  

    # Plotting the sentiment over time
    plt.figure(figsize=(10, 6))
    for sentiment in ["positive", "neutral", "negative"]:
        plt.plot(df_time_sentiment.index, df_time_sentiment[sentiment], label=sentiment.capitalize())

    plt.legend(title="Sentiment")
    plt.xlabel("Date")
    plt.ylabel("Number of Opinions")
    plt.title("Sentiment Over Time with AI Milestones")
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object and return it as a base64 encoded string
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

def industry_sentiment_heatmap(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(results)

    # Exploding the 'category' field into separate rows if it's a list
    df_expanded = df.explode('category')

    # Extract polarity (assuming it's a list, so taking the first element if it's a list)
    df_expanded['polarity'] = df_expanded['polarity'].apply(lambda x: x[0] if isinstance(x, list) else x)

    # Create a pivot table to count the occurrences of each polarity for each industry
    heatmap_data = df_expanded.pivot_table(index="category", columns="polarity", aggfunc="size", fill_value=0)
    
    # Plotting the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, cmap="RdYlGn", annot=True, fmt="d")
    plt.title("Industry Sentiment Heatmap")
    plt.xlabel("Sentiment")
    plt.ylabel("Industry")

    # Save the plot to a BytesIO object and return it as a base64 encoded string
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')



def ai_sentiment_trends_across_sectors(results):
    if not results:  # Handle empty results
        # Generate the placeholder image
        placeholder_img = generate_placeholder_image()

        # Convert PIL Image to base64
        img_buf = BytesIO()
        placeholder_img.save(img_buf, format='PNG')  # Save image
        img_buf.seek(0)

        # Encode image to base64
        plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')
        return plot_url  # Return base64-encoded placeholder image
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(results)

    # Explode the 'category' field into separate rows if it's a list
    df_expanded = df.explode('category')

    # Ensure the 'date' field is extracted properly from the list (if it's in a list)
    df_expanded['date'] = df_expanded['date'].apply(lambda x: x[0] if isinstance(x, list) else x)

    # Convert 'date' to datetime format
    df_expanded['date'] = pd.to_datetime(df_expanded['date'], format='%d-%m-%Y', errors='coerce')

    # Drop rows where 'date' could not be converted
    df_expanded = df_expanded.dropna(subset=['date'])

    # Group by 'date' and 'category', count occurrences, and unstack to get trends
    df_trend = df_expanded.groupby(["date", "category"]).size().unstack(fill_value=0)

    # Plotting the trends across sectors
    plt.figure(figsize=(12, 6))
    for industry in df_trend.columns:
        plt.plot(df_trend.index, df_trend[industry], label=industry)

    plt.legend(title="Industry", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Number of Opinions")
    plt.title("AI Sentiment Trends Across Different Job Sectors")
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object and return it as a base64 encoded string
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf8')

