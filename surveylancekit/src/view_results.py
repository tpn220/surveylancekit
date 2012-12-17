import webapp2
import jinja2
import os
import categories
import items
import votes
from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#the module to manipulate the voting information present in the datastore and display the results of
#votes placed by various users on the items in different categories

class ViewResults(webapp2.RequestHandler):
    
    def get(self):       
        user = users.get_current_user()
        function_type = self.request.get('function', None)
        cat_name = self.request.get('cat_name', None)
        creator_name = self.request.get('creator_name', None)
    
        if function_type is None: #display a list of all categories and their creators, whos results can be viewd        
            all_categories_query = db.GqlQuery('SELECT * FROM category')
            all_categories = all_categories_query.get()
            if all_categories:
                template_values = {
                                   'user' : user.nickname(),
                                   'log_out_url' :  users.create_logout_url("/"),
                                   'all_categories' : all_categories_query 
                                   }
                template = jinja_environment.get_template('viewresults.html')
                self.response.out.write(template.render(template_values))
        else: #display the results of a particular category
            self.displayResults(user, cat_name, creator_name)
                        
    #display the results of a particular category (Item Name, Winning Votes, Losing Votes)
    def displayResults(self, user, cat_name, creator_name):
        items_of_cat_query = db.GqlQuery('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(creator_name, cat_name))
        items_of_cat = items_of_cat_query.get()
        results_to_display = []
        for item in items_of_cat_query: #calculate number of winning and losing votes
            winning_votes_query = db.GqlQuery('SELECT * FROM vote WHERE creator = \'%s\' AND category = \'%s\' AND winner = \'%s\'' %(creator_name, cat_name, item.name))
            losing_votes_query = db.GqlQuery('SELECT * FROM vote WHERE creator = \'%s\' AND category = \'%s\' AND loser = \'%s\'' %(creator_name, cat_name, item.name))
            
            item_result = {
                          'item' : item,
                          'winning' : winning_votes_query.count(),
                          'losing' : losing_votes_query.count()
                          }
            results_to_display.append(item_result)
            
        template_values = {
                           'cat_name' : cat_name,
                           'creator' : creator_name,
                           'user' : user.nickname(),
                           'log_out_url' :  users.create_logout_url("/"),
                           'cat_results' : results_to_display
                           }
        template = jinja_environment.get_template('viewcategoryresult.html')
        self.response.out.write(template.render(template_values))
        
        
app = webapp2.WSGIApplication([('/view_results.*', ViewResults)],
                              debug=True)

if __name__ == '__main__':
    pass