import sys
import json
from datetime import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API

from config import TWITTER_ACCESS, TWITTER_SECRET, \
                   TWITTER_CON_SECRET, TWITTER_CON_ACCESS, \
                   ES_INDEX, ES_TYPE
from settings import gmaps
from utils import get_category
from aes_es import es


class StreamListener(StreamListener):
    def __init__(self):
        self.count = 0
        self.limit = 150

    def on_data(self, data):
        try:
            if self.count < self.limit:
                tweet = json.loads(data)
                if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
                    location = tweet['user'].get('location')
                    tweet_id = str(tweet['id'])
                    geocode_result = gmaps.geocode(location)
                    # print geocode_result
                    tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                    raw_tweet = {
                        'user': tweet['user']['screen_name'],
                        'text': tweet_text,
                        'location': tweet['user']['location'],
                        'coordinates': geocode_result, 
                        'time': tweet['created_at'],
                        'category': get_category(tweet_text)
                    }
                    es.index(index=ES_INDEX, doc_type=ES_TYPE, id=tweet_id, body=raw_tweet)
                self.count += 1
            else:
                stream.disconnect()
        except Exception as e:
            pass


    def on_error(self, status):
        print status
        # sys.exit()


if __name__ == '__main__':
    while True:
        auth = OAuthHandler(TWITTER_CON_ACCESS, TWITTER_CON_SECRET)
        auth.set_access_token(TWITTER_ACCESS, TWITTER_SECRET)

        listener = StreamListener()
        stream = Stream(auth, listener)

        stream.filter(track=['sports', 'politics', 'business', 'music', 'tech', 'health', 'finance', 'india', 'books', 'celebrity'])