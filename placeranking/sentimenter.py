__author__ = 'pawel'

import json
import urllib
import urllib2
import logging

class Sentimenter:

    def getSentiment(self, opinion):

        url = "http://text-processing.com/api/sentiment/"
        data = {
            "text": opinion
        }

        data = urllib.urlencode(data)
        header = {
            # "X-Mashape-Authorization": "1y2AiayLrMcGIq22X5jbBijhEPWogUhz"
        }
        request = urllib2.Request(url, data, header)
        ans = json.load(urllib2.urlopen(request))
        probability = ans["probability"]
        log = ", ".join(("sentiment:", str(ans["label"]), str(probability["pos"]), str(probability["neg"]), str(probability["neutral"])))
        logging.error(log)

        return ans["label"], probability["pos"], probability["neg"], probability["neutral"]
