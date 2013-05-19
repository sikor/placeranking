__author__ = 'pawel'

from google.appengine.ext import db


class DictModel(db.Model):

    def toDict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class Opinion(DictModel):
    comment = db.StringProperty(required=True, multiline=True)
    isPositive = db.BooleanProperty(required=True)
    location = db.GeoPtProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    continent = db.StringProperty()
    country = db.StringProperty()
    region = db.StringProperty()
    city = db.StringProperty()


class Counter(DictModel):
    parentKey = db.StringProperty(required=True)
    areaName = db.StringProperty(required=True)
    countPos = db.IntegerProperty(required=True, default=0)
    countNeg = db.IntegerProperty(required=True, default=0)