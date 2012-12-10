from google.appengine.ext import db

class category(db.Model):
    name = db.StringProperty(required=True)
    creator = db.StringProperty(required=True)