import logging
from thread import _count
from placeranking.geocoding import Geocoder

__author__ = 'Pawel'

import json
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from placeranking.model import *
import placeranking.geocoding
from placeranking.sentimenter import getSentiment
import logging

parentPropOf = {'country': None, 'region': 'country'}


def addOpinion(comment, pCategoryName, lat, lon):
    pLocation = db.GeoPt(lat=lat, lon=lon)
    geocoder = Geocoder()
    details = geocoder.getDetailedPosition(lat, lon)
    comment = unicode(comment)
    categories = db.GqlQuery('select * from OurCategory where categoryName = :1', pCategoryName)
    category = None
    if categories.count() == 0:
        category = OurCategory(categoryName=pCategoryName)
        category.put()
    else:
        category = categories.get()

    if comment is u"":
        raise Exception("comment cant be empty")

    sentiment = getSentiment(comment)
    pSentiment = sentiment[0]
    pProbabilityPos = sentiment[1]
    pProbabilityNeg = sentiment[2]
    pProbabilityNeu = sentiment[3]
    logging.error(str((
        comment, pSentiment, pLocation, details.city, details.continent, details.country, details.region, category,
        pProbabilityPos, pProbabilityNeg, pProbabilityNeu)))
    opinion = Opinion(comment=comment, sentiment=pSentiment, location=pLocation, city=details.city,
                      continent=details.continent, country=details.country, region=details.region, category=category,
                      probabilityPos=pProbabilityPos, probabilityNeg=pProbabilityNeg, probabilityNeu=pProbabilityNeu)
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

        if pSentiment == 'Positive':
            entity.countPos += 1
        elif pSentiment == 'Negative':
            entity.countNeg += 1
        entity.put()
    print opinion
    opinion.put()