import webapp2
import jinja2
import os
from google.appengine.ext import db
from google.appengine.api import users
import categories
import surveyusers
import items
import votes
import logging
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class ManageCategory(webapp2.RequestHandler):
    
    def rendering(self, user):
        parent_categories = db.GqlQuery('SELECT * FROM category where creator = \'%s\'' %user.nickname())
                
        template_values = {
                           'user' : user.nickname(),
                           'log_out_url' :  users.create_logout_url("/"),
                           'parent_categories' : parent_categories
                           }
        template = jinja_environment.get_template('managecategory.html')
        self.response.out.write(template.render(template_values))
                
    def post(self):
        user = users.get_current_user()
        new_cat_name = self.request.get('newcatname', None)
        item_name = self.request.get('newitemname', None)
        #import_cat_path = self.request.get('importcatpath', None)
        #if import_cat_path is None:
        if item_name is None:
            if new_cat_name is not None:
                check_if_cat_exists_query = db.GqlQuery('SELECT * FROM category WHERE creator = \'%s\' AND name = \'%s\'' %(user.nickname(), new_cat_name))
                check_if_cat_exists = check_if_cat_exists_query.get()
                if not check_if_cat_exists:
                    new_category = categories.category(name=new_cat_name, creator=user.nickname())
                    new_category.put()
                self.rendering(user)
        else:
            category_name = self.request.get('cat_name', None)
            check_if_item_exists_query = db.GqlQuery('SELECT * FROM item WHERE name = \'%s\' AND creator = \'%s\' AND category = \'%s\'' %(item_name, user.nickname(), category_name))
            check_if_item_exists = check_if_item_exists_query.get()
            if not check_if_item_exists:
                new_item = items.item(name=item_name, creator=user.nickname(), category=category_name)
                new_item.put()
            self.editCategory(category_name, user)
            #tree = xml.ElementTree()
            
        #    if category is not None:
        #        parse_cat_name = rootElement.find("NAME")
        #        items_list = category.findall("./CATEGORY/ITEM")
        #        self.parseCategoryFromXML(user, parse_cat_name, items_list)
                
    
    def parseCategoryFromXML(self, user, cat_name, items_list):
        cat_to_parse_query = db.GqlQuery('SELECT * FROM category WHERE creator = \'%s\' AND name = \'%s\'' %(user.nickname(), cat_name))
        cat_to_parse = cat_to_parse_query.get()
        if cat_to_parse:
            print "yes"
        else:
            new_category = categories.category(name=cat_name, creator=user.nickname())
            new_category.put()
            for item in items_list:
                new_item = items.item(name=item.attrib, creator=user.nickname(), category=cat_name)
                new_item.put()
                
        self.rendering(user)
                
    
    def get(self):       
        user = users.get_current_user()
          
        if user:
            function_type = self.request.get('function', None)
            cat_name = self.request.get('cat_name', None)
            item_name = self.request.get('item_name', None)
            parent_user = surveyusers.surveyuser.get_by_key_name(user.user_id())
            
            if item_name is None:
                if function_type == 'edit':
                    self.editCategory(cat_name, user)
                else:
                    if function_type == 'delete':
                        cat_to_delete_query = db.GqlQuery('SELECT * FROM category WHERE creator = \'%s\' AND name = \'%s\'' %(user.nickname(), cat_name))
                        items_cat_to_delete_query = db.GqlQuery('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(user.nickname(), cat_name))
                        votes_to_delete_query = db.GqlQuery('SELECT * FROM vote WHERE creator = \'%s\' AND category = \'%s\'' %(user.nickname(), cat_name))
                        votes_to_delete = votes_to_delete_query.get()
                        cat_to_delete = cat_to_delete_query.get()
                        items_cat_to_delete = items_cat_to_delete_query.get()
                        if cat_to_delete:
                            cat_to_delete.delete()
                        if items_cat_to_delete:
                            for item in items_cat_to_delete_query:
                                item.delete()
                        if votes_to_delete:
                            for vote in votes_to_delete_query:
                                vote.delete()
                        
                
                    self.rendering(user)
            else:
                if function_type == 'rename':
                    self.renameItem(user, cat_name, item_name)
                elif function_type == 'delete':
                    self.deleteItem(user, cat_name, item_name)
                self.editCategory(cat_name, user)
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def renameItem(self, user, cat_name, item_name):
        item_to_rename_query = db.GqlQuery('SELECT * FROM item WHERE name = \'%s\' AND creator = \'%s\' AND category = \'%s\'' %(item_name, user.nickname(), cat_name))
        item_to_rename = item_to_rename_query.get()
        item_to_rename.name = 'ABC'
        item_to_rename.put()
        
            
    def deleteItem(self, user, cat_name, item_name):
        item_to_delete_query = db.GqlQuery('SELECT * FROM item WHERE name = \'%s\' AND creator = \'%s\' AND category = \'%s\'' %(item_name, user.nickname(), cat_name))
        item_to_delete = item_to_delete_query.get()
        votes_to_delete_winner_query = db.GqlQuery('SELECT * FROM vote WHERE creator = \'%s\' AND category = \'%s\' AND winner = \'%s\'' %(user.nickname(), cat_name, item_to_delete.name))        
        votes_to_delete_loser_query = db.GqlQuery('SELECT * FROM vote WHERE creator = \'%s\' AND category = \'%s\' AND loser = \'%s\'' %(user.nickname(), cat_name, item_to_delete.name))
        votes_to_delete_winner = votes_to_delete_winner_query.get()
        votes_to_delete_loser = votes_to_delete_loser_query.get()
        if item_to_delete:
            item_to_delete.delete()
        if votes_to_delete_winner:
            votes_to_delete_winner.delete()
        if votes_to_delete_loser:
            votes_to_delete_loser.delete()
            
    def editCategory(self, cat_name, user):
        category_items = db.GqlQuery('SELECT * FROM item WHERE creator = \'%s\' AND category = \'%s\'' %(user.nickname(), cat_name))
        #self.response.write(category_items[0].name())
        
        template_values = {
                           'category' : cat_name,
                           'category_items' : category_items
                           }
        template = jinja_environment.get_template('editcategory.html')
        self.response.out.write(template.render(template_values))
    
            
app = webapp2.WSGIApplication([('/manage_category.*', ManageCategory)],
                              debug=True)

if __name__ == '__main__':
    pass