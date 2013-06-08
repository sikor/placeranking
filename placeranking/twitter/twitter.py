from placeranking.twitter import TwitterSearch, TwitterSearchOrder, TwitterSearchException
import logging
__author__ = 'pawel'

customer = "BmxcBtrl9jM1oOs68z1Q"
customer_secret = "W5q9G6SwGraGb6sddthTr7pEUP7Ps18pPJBcJTGs"
token = "1441295683-FyAw56ettjrdpYdQMXpUSv3PRYInfgolj1TCZih"
token_secret = "OBppMl2rGGXYisp9cViGDNGX6bq1es6CoYLaKPl2XU"


def getTweets(query, maxCount=20):
    try:
        tso = TwitterSearchOrder.TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.setKeywords([query]) # let's define all words we would like to have a look for
        tso.setLanguage('en') # we want to see German tweets only
        tso.setCount(maxCount) # please dear Mr Twitter, only give us 1 results per page
        tso.setIncludeEntities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch.TwitterSearch(
            consumer_key=customer,
            consumer_secret=customer_secret,
            access_token=token,
            access_token_secret=token_secret
        )

        ts.authenticate() # we need to use the oauth authentication first to be able to sign messages
        counter = 0
        for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
            try:
                counter += 1
                if counter == maxCount:
                    break
                logging.info('@%s tweeted: %s' % (tweet['user']['screen_name'].encode('ascii', 'replace'), tweet['text'].encode('ascii', 'replace')))
                yield tweet['text']
            except Exception as e:
                print e.message

    except TwitterSearchException, e: # take care of all those ugly errors if there are some
        print e.message