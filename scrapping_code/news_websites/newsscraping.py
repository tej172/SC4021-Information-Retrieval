import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from newspaper import Article
from fake_useragent import UserAgent

# Topics to search
TOPICS = [
    "AI replacing jobs",
    "Automation job loss",
    "Future of work AI",
    "AI layoffs",
    "AI hiring trends",
    "Tech layoffs",
    "AI in the workplace",
    "AI and employment",
    "Robots taking jobs",
    "Future of work with AI",
    "Artificial Intelligence impact on jobs",
    "AI automation and job displacement"
]

# News Sources with Correct URLs
NEWS_SOURCES = {
    "Google News": "https://www.google.com/search?q={query}&tbm=nws&start={page}",
    "Google Search": "https://www.google.com/search?q={query}&start={page}",
    "Reuters": "https://www.reuters.com/search/news?blob={query}&page={page}",
    "MIT Tech Review": "https://www.technologyreview.com/search/?s={query}&page={page}",
    "Wired": "https://www.wired.com/search/?q={query}&page={page}",
    "BBC": "https://www.bbc.co.uk/search?q={query}&page={page}",
    "Bloomberg": "https://www.bloomberg.com/search?query={query}&page={page}",
    "NYTimes": "https://www.nytimes.com/search?query={query}&page={page}",
    "TechCrunch": "https://techcrunch.com/search/{query}/page/{page}/",
    "The Verge": "https://www.theverge.com/search?q={query}&page={page}",
    "CNBC": "https://www.cnbc.com/search/?query={query}&page={page}",
    "Forbes": "https://www.forbes.com/search/?q={query}&page={page}"
}

# Setup Fake User-Agent for Web Requests
ua = UserAgent()
HEADERS = {
    "User-Agent": ua.random
}

def scrape_google_results(query, source_name):
    """Scrape Google Search results for news articles."""
    print(f"🔍 Fetching {source_name} results for: {query}")

    articles = []
    for page in range(0, 50, 10):  # Paginate for more results
        url = NEWS_SOURCES[source_name].format(query=query.replace(" ", "+"), page=page)
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"⚠️ Error fetching {source_name}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.find_all("a", href=True):
            try:
                title = item.text.strip()
                link = item["href"]
                if link.startswith("http") and "google.com" not in link:
                    articles.append({
                        "source": source_name,
                        "title": title,
                        "url": link,
                        "full_article": extract_full_article(link)
                    })
            except Exception:
                continue

        time.sleep(1)

    return articles

def scrape_news_source(query, source_name):
    """Scrape multiple pages from a news source."""
    print(f"🔍 Fetching {source_name} news for: {query}")

    articles = []
    for page in range(1, 5):  # Paginate
        url = NEWS_SOURCES[source_name].format(query=query.replace(" ", "+"), page=page)

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            print(f"⚠️ Error fetching {source_name}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.find_all("a", href=True):
            try:
                title = item.text.strip()
                link = item["href"]
                if not link.startswith("http"):
                    link = f"https://{source_name.lower()}.com{link}"
                articles.append({
                    "source": source_name,
                    "title": title,
                    "url": link,
                    "full_article": extract_full_article(link)
                })
            except Exception:
                continue

        time.sleep(1)

    return articles

def extract_full_article(url):
    """Extract full article text using Newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception:
        return "⚠️ Full article extraction failed."

def scrape_all_news():
    """Scrape news and Google search results."""
    all_articles = []

    for topic in TOPICS:
        print(f"🔎 Searching for: {topic}")

        google_news = scrape_google_results(topic, "Google News")
        google_search = scrape_google_results(topic, "Google Search")
        reuters_news = scrape_news_source(topic, "Reuters")
        mit_news = scrape_news_source(topic, "MIT Tech Review")
        wired_news = scrape_news_source(topic, "Wired")
        bbc_news = scrape_news_source(topic, "BBC")
        bloomberg_news = scrape_news_source(topic, "Bloomberg")
        nytimes_news = scrape_news_source(topic, "NYTimes")
        techcrunch_news = scrape_news_source(topic, "TechCrunch")
        theverge_news = scrape_news_source(topic, "The Verge")
        cnbc_news = scrape_news_source(topic, "CNBC")
        forbes_news = scrape_news_source(topic, "Forbes")

        articles = (google_news + google_search + reuters_news + mit_news +
                    wired_news + bbc_news + bloomberg_news + nytimes_news +
                    techcrunch_news + theverge_news + cnbc_news + forbes_news)
        
        for article in articles:
            article["topic"] = topic  # Add topic for reference

        all_articles.extend(articles)
        time.sleep(2)  # Avoid rate limiting

    return all_articles

# Run the scraper
news_data = scrape_all_news()

# Save Data
with open("all_scraped_news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, indent=4)

df = pd.DataFrame(news_data)
df.to_csv("all_scraped_news_data.csv", index=False)

print(f"✅ {len(news_data)} articles saved!")