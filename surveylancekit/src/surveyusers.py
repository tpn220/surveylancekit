from google.appengine.ext import db

#to store information (if required) of users logging onto the appliation
class surveyuser(db.Model):
    name = db.StringProperty(required=True) #name of the user