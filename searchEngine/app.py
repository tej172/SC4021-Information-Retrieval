from flask import Flask, request, render_template, session
import pysolr
import spacy
import re
import time
from datetime import datetime
from plotVisuals import (
    wordCloud, word_cloud_polarity, polarityDistribution,
    sentiment_distribution_by_industry, industry_sentiment_heatmap, aspect_sentiment_analysis,
    source_distribution, sentiment_by_source, sentiment_over_time, popularity_vs_sentiment
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Solr setup
solr = pysolr.Solr('http://localhost:8983/solr/mycore', timeout=10)

# NLP model
nlp = spacy.load('en_core_web_sm')

# Constants
DEFAULT_RESULTS_PER_PAGE = 5
PAGINATION_RANGE = 1
ALL_CATEGORIES = [
    "Technology & IT", "Finance & Banking", "Healthcare & Pharmaceuticals", "Energy & Utilities",
    "Retail & E-Commerce", "Entertainment & Media", "Manufacturing & Engineering", "Transportation & Logistics",
    "Education & Training", "Legal & Compliance", "Real Estate & Property", "Marketing & Advertising",
    "Human Resources & Talent Management", "Agriculture & Environmental", "Consumer Goods & Services",
    "Sports, Fitness & Recreation", "Non-Profit & Social Services", "Aerospace & Defense"
]
ALL_CONCEPTS = [
    "Jobs & Careers",  
    "AI Tech",  
    "Job Market Trends",  
    "Finance",  
    "Mental Health",  
    "Education Training",  
    "Automation & Displacement",  
    "Policy & Governance",  
    "Recruitment Technology",  
    "Remote & Gig Work",  
    "Public Sentiment Discourse",  
    "Tech Company Trends"  
]
# Helper functions
def get_param(key, default=''):
    """Retrieve request parameter with default handling."""
    return request.args.get(key, default=default).strip() or '*'

def get_list_param(key):
    """Retrieve list parameter with wildcard default."""
    return request.args.getlist(key) or ["*"]

def get_date_param(key):
    date = request.args.get(key, default='').strip() or '*'
    if date!= "*":
        valid_date = datetime.strptime(date, '%Y-%m-%d')  # Expecting YYYY-MM-DD format
        date = valid_date.strftime('%Y-%m-%dT00:00:00Z')  # Convert to the desired format
    return date

def build_solr_params(request_args):
    """Construct Solr search parameters from request arguments."""
    query = request_args.get('q', '').strip()
    words = []
    if query:
        lemmatized = ' '.join([token.lemma_ for token in nlp(query)])
        words = re.findall(r'\b\w+\b', lemmatized)
    return {
        'q': f'text:*' if not query else f'text:({" OR ".join(words)}~)',
        'filters': [
            f'source:({" OR ".join(get_list_param("source"))})',
            f'polarity:({" OR ".join(get_list_param("polarity"))})',
            f'subjectivity:({" OR ".join(get_list_param("subjectivity"))})',
            f'category:({" OR ".join(get_list_param("category"))})',
            f'concepts:{" OR ".join(get_list_param("concepts"))}' if request.args.getlist("concepts") else'',
            f'date: [{get_date_param("date_from")} TO {get_date_param("date_to")}]',
            f'popularity:[{get_param("popularity_min")} TO {get_param("popularity_max")}]'
        ],
        'sort': f'{get_param("sort_field", "id_num")} {get_param("sort_order", "asc")}',
        'start': (int(request_args.get('page', 1)) - 1) * DEFAULT_RESULTS_PER_PAGE,
        'rows': DEFAULT_RESULTS_PER_PAGE
    }

def generate_visualizations(results):
    """Generate various sentiment-related visualizations."""
    visual_functions = [
        wordCloud, word_cloud_polarity, polarityDistribution,
        sentiment_distribution_by_industry, industry_sentiment_heatmap, aspect_sentiment_analysis,
        source_distribution, sentiment_by_source, sentiment_over_time, popularity_vs_sentiment
    ]
    for func in visual_functions:
        func(results)

@app.route('/', methods=['GET'])
def search():
    """Handle search requests and render results."""
    params = build_solr_params(request.args)
    
    # Check if search parameters have changed
    search_params = {
        'q': request.args.get('q', ''),
        'date_from': get_param('date_from'),
        'date_to': get_param('date_to'),
        'popularity_min': get_param('popularity_min'),
        'popularity_max': get_param('popularity_max'),
        'sort_field': get_param('sort_field', 'id_num'),
        'sort_order': get_param('sort_order', 'asc'),
        'sources': get_list_param('source'),
        'polarity': get_list_param('polarity'),
        'subjectivity': get_list_param('subjectivity'),
        'category': get_list_param('category'),
        'concepts': get_list_param('concepts')
    }
    if session.get('search_params') != search_params:
        session['search_params'] = search_params
        start_query = time.time() 
        all_results = solr.search(q=params['q'], fq=params['filters'], sort=params['sort'], rows=12372).docs
        query_duration = time.time() - start_query 
        print(f"Query Time: {query_duration:.3f} seconds")
        generate_visualizations(all_results)
    
    # Retrieve paginated results
    paginated_results = solr.search(q=params['q'], fq=params['filters'], sort=params['sort'], start=params['start'], rows=params['rows'])
    total_results = paginated_results.hits
    total_pages = (total_results + DEFAULT_RESULTS_PER_PAGE - 1) // DEFAULT_RESULTS_PER_PAGE
    current_page = int(request.args.get('page', 1))
    
    for result in paginated_results.docs:
        result['date'][0] = datetime.strptime(result['date'][0], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")
        result['category'] = ", ".join(result['category'])
        if 'concepts' in result:
            result['concepts'] = ", ".join(result['concepts'])
        if 'aspects' in result:
            result['aspects'] = ", ".join(result['aspects'])
        
    return render_template(
        'search.html',
        query=request.args.get('q', ''),
        **search_params,
        results=paginated_results.docs,
        page=current_page,
        results_per_page=DEFAULT_RESULTS_PER_PAGE,
        total_pages=total_pages,
        selected_categories = get_list_param('category'),
        selected_concepts = get_list_param('concepts'),
        total_results=total_results,
        start_page=max(1, current_page - PAGINATION_RANGE),
        end_page=min(total_pages, current_page + PAGINATION_RANGE),
        all_categories=ALL_CATEGORIES,
        all_concepts=ALL_CONCEPTS
    )

if __name__ == '__main__':
    app.run(debug=True)
