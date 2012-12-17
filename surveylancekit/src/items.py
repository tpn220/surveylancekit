from google.appengine.ext import db

class item(db.Model):#the different items that are added to a User's Category
    name = db.StringProperty(required=True) #name of the item
    category = db.StringProperty(required=True) #category the item belongs to
    creator = db.StringProperty(required=True) #creator of the category the item belongs to
    