__author__ = 'pawel'

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from placeranking.model import *
import json
import logging
from placeranking.sentimenter import *
import placeranking.opinionDao
import placeranking.twitter.twitter
from google.appengine.ext import deferred


class ImportHandler(webapp.RequestHandler):
    def post(self):
        pQuery = unicode(self.request.get('query'))
        pCategoryName = unicode(self.request.get('category'))
        pTLat = float(self.request.get('tlat'))
        pTLon = float(self.request.get('tlon'))
        if "includeSource" in self.request.arguments():
            pSLat = float(self.request.get('slat'))
            pSLon = float(self.request.get('slon'))
            distance = int(self.request.get('distance'))
            logging.info("include source is checked")
        else:
            pSLat = None
            pSLon = None
            distance = None

        pMaxCount = int(self.request.get('maxCount'))
        deferred.defer(placeranking.twitter.twitter.findTweets, pQuery, pCategoryName, pTLat, pTLon, pMaxCount, pSLat, pSLon, distance)
        self.redirect('/home')


def main():
    app = webapp.WSGIApplication([(r'.*', ImportHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
    main()