import json
from TwitterSearch import *

from config import TWITTER_ACCESS, TWITTER_SECRET, \
                   TWITTER_CON_SECRET, TWITTER_CON_ACCESS, \
                   ES_INDEX, ES_TYPE
from settings import gmaps, queue
# from settings import es
from utils import get_category


try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['sports', 'trump', 'clinton', 'india', 'china', 'politics',
        'castro', 'thanksgiving'], or_operator=True)
    tso.set_language('en')

    ts = TwitterSearch(
        consumer_key = TWITTER_CON_ACCESS,
        consumer_secret = TWITTER_CON_SECRET,
        access_token = TWITTER_ACCESS,
        access_token_secret = TWITTER_SECRET
     )

    count = 0
    
    for tweet in ts.search_tweets_iterable(tso):
        try:
            if tweet['user'].get('location') is not None and tweet['lang']=='en':
                place = tweet['user'].get('location')
                if place:
                    tweet_id = str(tweet['id'])
                    geocode_result = gmaps.geocode(place)
                    if len(geocode_result) > 0:
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']
                        tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                        raw_tweet = {
                            'tweet_id': tweet_id,
                            'user': tweet['user']['screen_name'],
                            'text': tweet_text,
                            'place': place,
                            'coordinates': {'location': str(lat)+","+str(lng)}, 
                            'time': tweet['created_at'],
                            'category': get_category(tweet_text)
                        }
                        queue.send_message(MessageBody=json.dumps(raw_tweet))
                    # es.index(index=ES_INDEX, doc_type=ES_TYPE, id=tweet_id, body=raw_tweet)
        except Exception as e:
            print e
            continue

except TwitterSearchException as e:
    print(e)