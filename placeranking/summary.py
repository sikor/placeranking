
__author__ = 'pawel'

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from placeranking.model import *
import json
import logging


class SummaryHandler(webapp.RequestHandler):
    def get(self):
        parent = self.request.get('parentKey')
        if not parent:
            parent = 'root'
            logging.error("parent = root")

        counters = db.GqlQuery('select * from Counter where parentKey= :parentKey', parentKey=parent).fetch(limit=1000)
        logging.error("counters "+str(len(counters)))
        jsonCounters = json.dumps(counters, default=lambda x: x.toDict())
        self.response.headers.add_header("Cache-Control", "no-store")
        self.response.out.write(jsonCounters)

def main():
    app = webapp.WSGIApplication([(r'.*', SummaryHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()