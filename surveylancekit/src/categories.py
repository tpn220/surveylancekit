from google.appengine.ext import db


#The model for each category created by a user
class category(db.Model):
    name = db.StringProperty(required=True) #Name of the category
    creator = db.StringProperty(required=True) #Creator of the category