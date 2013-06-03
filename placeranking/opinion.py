import logging
from thread import _count
from placeranking.geocoding import Geocoder

__author__ = 'Pawel'

import json
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from placeranking.model import *
from placeranking.sentimenter import Sentimenter
import placeranking.geocoding


parentPropOf = {'country': None, 'region': 'country'}

class OpinionHandler(webapp.RequestHandler):
    def get(self):
        opinions = db.GqlQuery('select * from Opinion order by when desc').fetch(limit=1000)

        jsonOpinions = json.dumps(opinions, default=lambda o: o.toDict())
        self.response.headers.add_header("Cache-Control", "no-store")
        self.response.out.write(jsonOpinions)


    def post(self):
        """


        :return:
        """
        pComment = unicode(self.request.get('comment'))
        pCategoryName = categoryName=unicode(self.request.get('category'))
        #TODO change it to more optimal


        categories = db.GqlQuery('select * from OurCategory where categoryName = :1', pCategoryName)
        category = None
        if categories.count() == 0:
            category = OurCategory(categoryName = pCategoryName)
            category.put()
        else:
            category = categories.get()
        pIsPositive = (self.request.get('isPositive') == 'True')
        pLat = float(self.request.get('lat'))
        pLon = float(self.request.get('lon'))
        pLocation = db.GeoPt(lat=pLat, lon=pLon)
        geocoder = Geocoder()
        details = geocoder.getDetailedPosition(pLat, pLon)
        if pComment is u"":
            self.response.write("Comment cannot be empty.")
            return
        opinion = Opinion(comment=pComment, isPositive=pIsPositive, location=pLocation, city=details.city,
                          continent=details.continent, country=details.country, region=details.region, category=category)

        for prop in details.properties():
            if prop in ['city', 'continent']:
                continue
            counter = Counter.all()
            key = getattr(details, prop)
            if not key:
                continue
            counter.filter("areaName =", key)
            entity = counter.get()
            parentProp = parentPropOf[prop]
            if entity is None:
                parentKey = getattr(details, str(parentProp), 'root')
                entity = Counter(areaName=key, parentKey=parentKey)

            if pIsPositive:
                entity.countPos += 1
            else:
                entity.countNeg += 1
            entity.put()

        opinion.put()
        self.redirect('/home')




application = webapp.WSGIApplication([(r'.*', OpinionHandler)], debug=True)


def main():
    app = webapp.WSGIApplication([(r'.*', OpinionHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
    main()