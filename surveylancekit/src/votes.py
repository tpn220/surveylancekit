from google.appengine.ext import db

#to store information about the votes placed on the items in a category by any user
class vote(db.Model):
    voter = db.StringProperty(required=True) #the user who has placed the vote
    creator = db.StringProperty(required=True) #the creator of the category that hold the items
    category = db.StringProperty(required=True) #the category that holds the items
    winner = db.StringProperty(required=True) #the winning vote (item)
    loser = db.StringProperty(required=True) #the losing vote (item)