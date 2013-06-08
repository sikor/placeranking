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

class ImportHandler(webapp.RequestHandler):
    def post(self):
        pQuery = unicode(self.request.get('query'))
        pCategoryName = unicode(self.request.get('category'))
        pLat = float(self.request.get('lat'))
        pLon = float(self.request.get('lon'))
        for tweet in placeranking.twitter.twitter.getTweets(pQuery):
            placeranking.opinionDao.addOpinion(tweet, pCategoryName, pLat, pLon)
        self.redirect('/home')


def main():
    app = webapp.WSGIApplication([(r'.*', ImportHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
    main()