
__author__ = 'pawel'

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from placeranking.model import Opinion, OurCategory



class MyHandler(webapp.RequestHandler):
    def get(self):
        opinionsQuery = db.GqlQuery('select * from Opinion order by when desc')
        categoriesQuery = db.GqlQuery('select * from OurCategory order by categoryName')

        values = {
            'opinions': opinionsQuery,
            'categories': categoriesQuery
        }
        self.response.headers.add_header("Cache-Control", "no-store")
        self.response.out.write(unicode(template.render('templates/main.html', values)))

    def post(self):
        opinion = Opinion(comment=str(self.request.get('comment')),
                          isPositive=(self.request.get('isPositive') == 'True'),
                          location=db.GeoPt(lat=50.0, lon=20.0))
        opinion.put()
        self.redirect('/home')


class Summary(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header("Cache-Control", "no-store")
        self.response.out.write(unicode(template.render('templates/summary.html', {})))


def main():
    app = webapp.WSGIApplication([('/summary', Summary), (r'.*', MyHandler), ], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()