from twikit import Client
from twikit import errors
from configparser import ConfigParser
import asyncio
import pprint
import time
from datetime import datetime
import csv
from random import randint

import json


MINIMUM_TWEETS=500
QUERY_TYPE = 'Latest' #Top', 'Latest' OR 'Media'

# JSON file path
json_file = 'scrape_x_test/tweets_data_2024_top.json'
# QUERY='AI job market until:2021-12-31 since:2021-01-01'
# QUERY='AI job market until:2022-12-31 since:2022-01-01'
# QUERY='AI job market until:2023-12-31 since:2023-01-01'4
QUERY='AI job market until:2024-12-31 since:2024-01-01'
# QUERY='AI job market'
# QUERY='AI job market "Layoff" (chatgpt OR LLMs OR LLM OR Agents OR Agentic OR Job loss OR layoffs OR Tech OR AI OR Downsizing)'
# QUERY='AI job market "jobloss" (chatgpt OR LLMs OR LLM OR Agents OR Agentic OR Job loss OR layoffs OR Tech OR AI OR Downsizing)'
# QUERY='AI job market "replace" (chatgpt OR LLMs OR LLM OR Agents OR Agentic OR Job loss OR layoffs OR Tech OR AI OR Downsizing)'
# QUERY='AI job market "downsizing" (chatgpt OR LLMs OR LLM OR Agents OR Agentic OR Job loss OR layoffs OR Tech OR AI OR Downsizing)'
# QUERY='AI job market "job cut" (chatgpt OR LLMs OR LLM OR Agents OR Agentic OR Job loss OR layoffs OR Tech OR AI OR Downsizing)'
# QUERY='AI job market "layoff" (#recruitment OR #jobsearch OR #AI OR #HRTech OR #Automation OR #ArtificialIntelligence OR #AIJobs OR #JobAutomation OR #JobCuts OR #Downsizing OR #FutureOfWork OR #TechLayoffs OR #Layoffs)'

# print(f"{errors.TooManyRequests}")

# Load login credentials
config = ConfigParser()
config.read('scrape_x_test/config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# Initialize the client
client = Client(language='en-US')

import os

# Ensure the directory exists
os.makedirs('scrape_x_test', exist_ok=True)

# # Create CSV file if it does not exist
# csv_file = 'scrape_x_test/tweets_data.csv'
# if not os.path.exists(csv_file):
#     with open(csv_file, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['Tweet Count', 'Username', 'Text', 'Created At', 'Retweet Count', 'Favorite Count'])


# Load existing data from JSON file (if exists)
if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            tweets_data = json.load(f)
        except json.JSONDecodeError:
            tweets_data = []
else:
    tweets_data = []


async def main():
    await client.login(
        auth_info_1=username,
        auth_info_2=email,
        password=password,
        cookies_file='scrape_x_test/cookies.json'
    )

    tweet_count = len(tweets_data)  # Start counting from the existing number of tweets
    tweets= None
    # tweets_data = []

    while tweet_count < MINIMUM_TWEETS:
        # Search for tweets

        try:

            if(tweets is None):
                print("==========================================")
                print(f"{datetime.now()}- Getting tweets") 
                print(f"Searching for tweets with the query: {QUERY}")
                print(f"Minimum tweets to scrape: {MINIMUM_TWEETS}")
                print("==========================================")

                tweets = await client.search_tweet(QUERY, product=QUERY_TYPE, count=min(MINIMUM_TWEETS,20))
            else:
                wait_time = randint(4, 44)
                print(f"{datetime.now()}- Waiting for {wait_time} seconds")
                await asyncio.sleep(wait_time)

                print(f"f{datetime.now()}- Getting next tweets")
                tweets = await tweets.next()
        except errors.TooManyRequests as e:
            rate_limit_reset=datetime.fromtimestamp(e.rate_limit_reset)
            print(f"{datetime.now()}- Rate limit reached. Waiting until {rate_limit_reset}")
            new_wait_time= e.rate_limit_reset - time.time()
            await asyncio.sleep(new_wait_time)
            continue #continue to the next iteration of the loop

        if not tweets:
            print(f"{datetime.now()}- No tweets found")
            break
        

        for tweet in tweets:
            tweet_count += 1
            tweet_data = {
                "tweet_count": tweet_count,
                "username": tweet.user.name,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "favorite_count": tweet.favorite_count,
                "retweet_count": tweet.retweet_count
            }
            tweets_data.append(tweet_data)
            # scrapped_tweet= [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            # print(
            #     # pprint.pprint(vars(tweet))
            #     pprint.pprint(scrapped_tweet)
            #     # tweet.user.name,
            #     # tweet.text,
            #     # tweet.created_at,
            #     # "=======\n"
            # )

            # with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(scrapped_tweet) #write the scrapped tweet to the csv file
            # Save to JSON file (appending)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(tweets_data, f, indent=4)
        print(f"{datetime.now()}- Total tweets scrapped in this loop: {tweet_count}")

    print("==========================================")
    print(f"{datetime.now()} - DOne tweets from X.com..Got {tweet_count} tweets")
    print("==========================================")
asyncio.run(main())
