__author__ = 'Pawel'


import json
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from placeranking.model import Opinion


class OpinionHandler(webapp.RequestHandler):
    def get(self):
        opinions = db.GqlQuery('select * from Opinion order by when desc').fetch(limit=1000)
        jsonOpinions = json.dumps(opinions, default=lambda o: o.toDict())
        self.response.headers.add_header("Cache-Control", "no-store")
        self.response.out.write(jsonOpinions)

    def post(self):
        pComment = unicode(self.request.get('comment'))
        pIsPositive = (self.request.get('isPositive') == 'True')
        pLat = float(self.request.get('lat'))
        pLon = float(self.request.get('lon'))
        pLocation = db.GeoPt(lat=pLat, lon=pLon)
        opinion = Opinion(comment=pComment, isPositive=pIsPositive, location=pLocation)
        opinion.put()
        self.redirect('/home')


application = webapp.WSGIApplication([(r'.*', OpinionHandler)], debug=True)


def main():
    app = webapp.WSGIApplication([(r'.*', OpinionHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()