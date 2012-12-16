import webapp2
import jinja2
import os
import random
import logging
from google.appengine.ext import db
from google.appengine.api import users
import categories
import surveyusers
import items
import votes

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class VoteCategory(webapp2.RequestHandler):
    
    def renderingVotePage(self, user):
        all_categories = db.GqlQuery('SELECT * FROM category')
        catsWithAtleastTwoItems = []
        for category in all_categories:
            items_of_category = db.GqlQuery('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(category.creator, category.name))
            if items_of_category.count() >= 2:
                catsWithAtleastTwoItems.append(category)
        
        template_values = {
                           'user' : user.nickname(),
                           'all_categories' : catsWithAtleastTwoItems
                           }
        template = jinja_environment.get_template('votecategory.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        user = users.get_current_user()
        winning_choice = self.request.get('voteforitem', None)
        first_choice_item = self.request.get('firstchoiceitem', None)
        second_choice_item = self.request.get('secondchoiceitem', None)
        cat_name = self.request.get('cat_name', None)
        creator_name = self.request.get('creator_name', None)
        category_query = db.GqlQuery('SELECT * FROM category WHERE name = \'%s\' AND creator = \'%s\'' %(cat_name, creator_name))
        category = category_query.get()
        losing_choice = ''
        
        if winning_choice == first_choice_item:
            losing_choice = second_choice_item
        else:
            losing_choice = first_choice_item
        
        #logging.debug('USERRRR %s' %creator_name)    
        new_vote = votes.vote(voter=user.nickname(), creator=creator_name, category=cat_name, winner=winning_choice, loser=losing_choice)
        new_vote.put()
        self.voteOnCategory(user, cat_name, creator_name)
    
    def get(self):       
        user = users.get_current_user()
        
        if user:
            function_type = self.request.get('function', None)
            cat_name = self.request.get('cat_name', None)
            creator_name = self.request.get('creator_name', None)
            
            if function_type == 'vote':
                self.voteOnCategory(user, cat_name, creator_name)
            else:
                self.renderingVotePage(user)
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def voteOnCategory(self, user, cat_name, creator_name):
        #to_vote_category_query = db.GqlQuery('SELECT * FROM category WHERE creator = \'%s\' AND name = \'%s\'' %(user.nickname(), cat_name))
        #to_vote_category = to_vote_category_query.get()
        items_of_category = db.GqlQuery('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(creator_name, cat_name))
        #items_of_category = items_of_category_query.get()
        #logging.debug('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(creator_name, cat_name))
        rand_list = []
        for item in items_of_category:
            rand_list.append(item)
        items_choices = random.sample(rand_list, 2)
        
        template_values = {
                         'category' : cat_name,
                         'creator_name' : creator_name,
                         'item_choice_one' : items_choices[0],
                         'item_choice_two' : items_choices[1]
                         }
        template = jinja_environment.get_template('placevotes.html')
        self.response.out.write(template.render(template_values))
            
app = webapp2.WSGIApplication([('/vote_category.*', VoteCategory)],
                              debug=True)

if __name__ == '__main__':
    pass