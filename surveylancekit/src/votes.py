from google.appengine.ext import db

class vote(db.Model):
    voter = db.StringProperty(required=True)
    creator = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    winner = db.StringProperty(required=True)
    loser = db.StringProperty(required=True)