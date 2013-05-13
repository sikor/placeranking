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