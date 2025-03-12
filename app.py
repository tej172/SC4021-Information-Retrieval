from flask import Flask, request, render_template
import pysolr
from plotVisuals import wordCloud, plotGraph1, plotGraph2,polarityDistribution
import json
import plotly
import plotly.graph_objs as go

app = Flask(__name__)

# Solr connection URL
SOLR_URL = 'http://localhost:8983/solr/mycore'

# Initialize a Solr client
solr = pysolr.Solr(SOLR_URL, timeout=10)


@app.route('/', methods=['GET'])
def search():
    # Get the search query
    query = request.args.get('q', '').strip()  # Default to '*' if 'q' is not found

    # Get the date range
    date_from = request.args.get('date_from', '').strip() or '*'  # Default to '*' if 'date_from' is not found
    date_to = request.args.get('date_to', '').strip() or '*'  # Default to '*' if 'date_to' is not found

    # Get the popularity range
    popularity_min = request.args.get('popularity_min', '').strip() or '*'  # Default to '*' if 'popularity_min' is not found
    popularity_max = request.args.get('popularity_max', '').strip() or '*'  # Default to '*' if 'popularity_max' is not found

    # Get the sorting options
    sort_field = request.args.get('sort_field', '').strip() or 'id'  # Default to 'popularity' if 'sort_field' is not found
    sort_order = request.args.get('sort_order', '').strip() or 'asc'  # Default to 'desc' if 'sort_order' is not found

    # Get the sources
    sources = request.args.getlist('source') or ["*"]  # Default to ['*'] if list not found

    # Get the polarities
    polarities = request.args.getlist('polarity') or ["*"]  # Default to ['*'] if list not found

    # Get the subjectivities
    subjectivities = request.args.getlist('subjectivity') or ["*"]  # Default to ['*'] if list not found

    # Get the selected categories
    selected_categories = request.args.getlist('category') or ["*"]  # Default to ['*'] if list not found

    # Get the page number and results per page
    page = int(request.args.get('page', 1))
    results_per_page = int(request.args.get('results_per_page', 5))

    # Define the list of all available categories
    all_categories = [
        "Technology & IT",
        "Finance & Banking",
        "Healthcare & Pharmaceuticals",
        "Energy & Utilities",
        "Retail & E-Commerce",
        "Entertainment & Media",
        "Manufacturing & Engineering",
        "Transportation & Logistics",
        "Education & Training",
        "Legal & Compliance",
        "Real Estate & Property",
        "Marketing & Advertising",
        "Human Resources & Talent Management",
        "Agriculture & Environmental",
        "Consumer Goods & Services",
        "Sports, Fitness & Recreation",
        "Non-Profit & Social Services",
        "Aerospace & Defense"
    ]

  
    # Perform the search if there's a query
    results = []
    total_results = 0
    # Define query parameters
    params = {
        'q': f'text:*{query}*',
        'fq': [
            f'source:({" OR ".join(sources)})',
            f'polarity:({" OR ".join(polarities)})',
            f'subjectivity:({" OR ".join(subjectivities)})',
            f'category:({" OR ".join(selected_categories)})',
            f'date:[{date_from} TO {date_to}]',
            f'popularity:[{popularity_min} TO {popularity_max}]'
        ],
        'sort': f'{sort_field} {sort_order}',
        'start': (page - 1) * results_per_page,
        'rows': results_per_page
    }

    # Perform the search
    search_results = solr.search(q=params['q'], fq=params['fq'], sort=params['sort'], start=params['start'], rows=params['rows'])
    results = search_results.docs  # Extract documents from the search results
    total_results = search_results.hits  # Total number of results
    # Calculate total pages
    total_pages = (total_results + results_per_page - 1) // results_per_page

    # Generate Result Specific Graph
    # Example Plotly graph 1 # plotGraph1()
    graph1_json = polarityDistribution(results)
    plot_url1 = wordCloud(results)

    # Render the HTML template with the query and results
    return render_template('search.html', 
                         query=query, 
                         date_from=date_from, 
                         date_to=date_to, 
                         popularity_min=popularity_min, 
                         popularity_max=popularity_max, 
                         sort_field=sort_field, 
                         sort_order=sort_order, 
                         sources=sources, 
                         polarities=polarities, 
                         subjectivities=subjectivities, 
                         selected_categories=selected_categories, 
                         all_categories=all_categories, 
                         results=results,
                         page=page,
                         results_per_page=results_per_page,
                         total_pages=total_pages,
                         total_results=total_results,
                         graph1_json=graph1_json, 
                         plot_url1=plot_url1)

if __name__ == '__main__':
    app.run(debug=True)