from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 500
QUERY = 'Ai replace jobs'


def get_tweets(tweets):
    if tweets is None:
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Text'])

client = Client(language='en-US')
#login first time will generate cookies
#client.login(auth_info_1=username,auth_info_2=email,password=password)
#client.save_cookies('cookies.json')
client.load_cookies('cookies.json')

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print('No more tweets found')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.text]
        
        with open('tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)


print(f'{tweet_count} tweets found')