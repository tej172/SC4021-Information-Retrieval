

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
# Ensure that NLTK data is downloaded
#nltk.download('punkt_tab')
#nltk.download('stopwords')
#nltk.download('vader_lexicon')
'''
[{'id': '1', 'text': ['If ai speeds up work or even regularly does a single task, that displaces jobs.\n\nReduced workload -> reduced headcount'], 
  'time': [1718039224.0], 'popularity': [463], 
  'source': ['Reddit'], 
  'polarity': ['negative'], 
  'subjectivity': ['neutral'],
  'category': ['Technology & IT', 'Consumer Goods & Services', 'Non-Profit & Social Services', 'Manufacturing & Engineering', 'Human Resources & Talent Management'], 
  'date': ['2024-06-10'], '_version_': 1826306439897939968, '_root_': '1'},.....]
'''

def wordCloud(results):
    try:
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
        plt.figure(figsize=(12, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        # Save the image to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=500)  # Higher DPI for quality
        img.seek(0)

        # Encode the image to base64 to pass it to HTML
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return plot_url  # Return base64 string of the word cloud image
    finally:
        plt.close()  # Ensure plt.close() is called to release memory


def plotGraph1(result2):
    # Example Plotly graph 1
    graph1 = go.Figure(data=[go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines')])
    return json.dumps(graph1, cls=plotly.utils.PlotlyJSONEncoder)

def plotGraph2(result2):
    # Example Plotly graph 2
    graph2 = go.Figure(data=[go.Pie(labels=['A', 'B', 'C'], values=[40, 30, 30])])
    return json.dumps(graph2, cls=plotly.utils.PlotlyJSONEncoder)

def polarityDistribution(results):
    
    positive = negative = neutral = 0
    for post in results:
        if post['polarity'][0] == 'positive':
            positive +=1 
        elif post['polarity'][0] == 'negative':
            negative +=1
        else : # post['polarity'][0] == 'neutral'
            neutral +=1

    data = {
    'positive':  positive,
    'neutral':  neutral,
    'negative':  negative
    }   
    # Create the bar graph
    categories = list(data.keys())
    values = list(data.values())
    # Define common properties for both traces
    common_props = dict(
        labels=categories,
        values=values,
        marker=dict(colors=['green','gray','red'])  # Custom color sequence
    )

    # First trace: showing percentage outside
    trace1 = go.Pie(
        **common_props,
        textinfo='label',
        textposition='outside',
        textfont=dict(size=14, color="black"),
        sort = False
    )

    # Second trace: showing category labels inside
    trace2 = go.Pie(
        **common_props,
        textinfo='percent + value',
        textposition='inside',
        textfont=dict(size=14, color="black"),
        sort = False
    )

    # Create the figure with both traces overlapping
    fig = go.Figure(data=[trace1, trace2],)

    # Remove the legend
    fig.update_layout(showlegend=False, 
                      title_text= "Polarity Composition",
                      font=dict(size=16))
    
    # Show the pie chart
    #fig.show()
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)