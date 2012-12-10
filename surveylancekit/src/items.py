from google.appengine.ext import db

class item(db.Model):
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    creator = db.StringProperty(required=True)
    