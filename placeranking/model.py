__author__ = 'pawel'

from google.appengine.ext import db


class DictModel(db.Model):
    def toDict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class OurCategory(DictModel):
    categoryName = db.StringProperty(required=True)

class Opinion(DictModel):
    comment = db.StringProperty(required=True, multiline=True)
    sentiment = db.StringProperty(required=True)
    probabilityNeg = db.FloatProperty(required=True)
    probabilityPos = db.FloatProperty(required=True)
    probabilityNeu = db.FloatProperty(required=True)
    location = db.GeoPtProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    continent = db.StringProperty()
    country = db.StringProperty()
    region = db.StringProperty()
    city = db.StringProperty()
    category = db.ReferenceProperty(OurCategory)


class Counter(DictModel):
    parentKey = db.StringProperty(required=True)
    areaName = db.StringProperty(required=True)
    countPos = db.IntegerProperty(required=True, default=0)
    countNeg = db.IntegerProperty(required=True, default=0)


