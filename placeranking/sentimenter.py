__author__ = 'pawel'

import json
import urllib
import urllib2
import logging
from sentiement.sentiment import SentimentAnalyzer


sentimentAnalyzer = SentimentAnalyzer()
sentimentAnalyzer.train()

def getSentiment(opinion):

    url = "http://text-processing.com/api/sentiment/"
    data = {
        "text": opinion.encode('ascii', 'ignore')
    }

    data = urllib.urlencode(data)
    header = {
        # "X-Mashape-Authorization": "1y2AiayLrMcGIq22X5jbBijhEPWogUhz"
    }
    request = urllib2.Request(url, data, header)
    ans = json.load(urllib2.urlopen(request))
    probability = ans["probability"]
    log = ", ".join(("sentiment:", str(ans["label"]), str(probability["pos"]), str(probability["neg"]), str(probability["neutral"])))
    logging.info(log)
    if ans["label"] in set(["Neutral, pos, neg"]):
        return "neutral", 0, 0, 0

    return str(ans["label"]), probability["pos"], probability["neg"], probability["neutral"]


def getSentimentOffline(opinion):
    prob = sentimentAnalyzer.analyze(opinion)
    sentiment = 'pos' if prob.prob('pos') > prob.prob('neg') else 'neg'
    logging.info('%s : %d' % (sentiment, prob.prob(sentiment)))
    if prob.prob(sentiment) < 0.6:
        sentiment = 'neutral'

    return sentiment, prob.prob('pos'), prob.prob('neg'), 0.0



