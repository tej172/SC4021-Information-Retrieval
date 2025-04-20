from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
from bs4 import BeautifulSoup

# LinkedIn Credentials (USE ENV VARIABLES FOR SECURITY)
USERNAME = config['Link']['username']
PASSWORD = config['Link']['password']

# Expanded list of topics
TOPICS = [
    "AI replacing jobs",
    "Automation job loss",
    "Future of work AI",
    "AI layoffs",
    "AI hiring trends",
    "AI and employment",
    "Robots taking jobs",
    "AI in the workplace",
    "AI and job security",
    "Future jobs with AI",
    "Tech layoffs",
    "Job displacement due to AI",
    "AI and the gig economy",
    "AI workforce automation",
    "AI and human jobs",
    "AI vs. human workers",
    "Reskilling for AI",
    "AI job predictions 2025",
    "AI and white-collar jobs",
    "AI replacing blue-collar jobs",
    "AI job predictions", 
    "ChatGPT and jobs",
    "ChatGPT replaces jobs",
    "OpenAI and jobs", 
    "Gemini and jobs",
    "LLMs replace jobs"
]

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # Run in headless mode (remove if debugging)

driver = webdriver.Chrome(options=options)

def login():
    """Log into LinkedIn."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    try:
        username_input = driver.find_element("name", "session_key")
        password_input = driver.find_element("name", "session_password")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete
    except Exception as e:
        print(f"⚠️ Error logging in: {e}")
        driver.quit()

def search_posts(topic):
    """Search for posts related to a specific topic."""
    search_url = f"https://www.linkedin.com/search/results/content/?keywords={topic.replace(' ', '%20')}&origin=SWITCH_SEARCH_VERTICAL"
    driver.get(search_url)
    time.sleep(5)

def infinite_scroll(max_scrolls=150):
    """Scroll continuously to load more posts."""
    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop if no new posts load
        last_height = new_height

def extract_posts(topic):
    """Extract posts with additional metadata."""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.find_all("div", class_="feed-shared-update-v2")  # Ensure the class matches LinkedIn's latest update

    data = []
    for post in posts:
        try:
            text = post.find("span", class_="break-words").text.strip()
            timestamp = post.find("span", class_="visually-hidden").text.strip()
            likes_element = post.find("span", class_="social-details-social-counts__reactions-count")
            likes = likes_element.text.strip() if likes_element else "0"

            # Extract author name
            author = post.find("span", class_="feed-shared-actor__name").text.strip() if post.find("span", class_="feed-shared-actor__name") else "Unknown"

            # Extract post URL
            post_url = post.find("a", href=True)["href"] if post.find("a", href=True) else "No URL"

            # Prioritize high-engagement posts
            if int(likes.replace(",", "")) >= 5:  # Keep only posts with 5+ likes
                data.append({
                    "topic": topic,
                    "author": author,
                    "text": text,
                    "timestamp": timestamp,
                    "likes": likes,
                    "post_url": f"https://www.linkedin.com{post_url}"
                })
        except AttributeError:
            continue

    return data

def save_data(data, topic):
    """Save crawled data to JSON & CSV."""
    json_filename = f"linkedin_{topic.replace(' ', '_')}.json"
    csv_filename = f"linkedin_{topic.replace(' ', '_')}.csv"

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)

# Run the crawler for each topic
login()

for topic in TOPICS:
    print(f"🔍 Searching for posts on: {topic}")
    search_posts(topic)
    infinite_scroll(max_scrolls=150)  # Scroll up to 150 times (expandable)
    posts_data = extract_posts(topic)
    save_data(posts_data, topic)
    print(f"✅ {len(posts_data)} posts saved for topic: {topic}\n")
    time.sleep(10)  # Delay between searches to avoid detection

print("🎉 Data collection complete!")
driver.quit()