import requests
from requests_oauthlib import OAuth1
from app.settings import API_KEY, API_SECRET_KEY
from app.main.utils.helpers.commons import get_trace
import json


def top_tweets(cache: object, count: int):
    """
    This method will return top-tweets
    comming from the request or just the cache

    params : the cache for the context
    return boolean telling if everything went well [top-tweets] as string
    """

    if cache.get("top-tweets") is None:
        try:
            # we make another request
            # to the twitter api
            print(">> Hitting twitter api...")

            search_twitter_host = "https://api.twitter.com/1.1/search/tweets.json"
            tweets = requests.get(
                "{}?q=%23caparledev%20-filter%3Aretweets&count={}".format(search_twitter_host, str(count)),
                auth=OAuth1(API_KEY, API_SECRET_KEY)
            ).content.decode()

            # and we cache it as json string for 1h
            cache.set("top-tweets", tweets, 3600)
        except Exception:
            # We just print the trace-back here
            get_trace()
            return (False, cache.get("top-tweets"))
    else:
        print("<< Getting from cache...")

    return (True, cache.get("top-tweets"))


def get_top_tweets(cache: object, count: int):
    """
    This method will check the return of top-tweet and send
    the appropriate status code for the request

    """

    results = top_tweets(cache, count)

    if results[0]:
        payload = json.loads(results[1])
        if "errors" in payload:
            return {
                "code": 500,
                "status": "error",
                "result": payload
            }
        else:
            return {
                "code": 200,
                "status": "success",
                "result": payload
            }
    else:
        return {
            "code": 500,
            "status": "error"
        }
