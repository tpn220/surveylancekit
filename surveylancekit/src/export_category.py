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
import urllib2
import xml.etree.ElementTree as ET

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# Module to export a category to an xml file

class ExportCategory(webapp2.RequestHandler):
    
    def get(self):       
        user = users.get_current_user()
          
        if user: #checks if user is logged in
            function_type = self.request.get('function', None)
            cat_name = self.request.get('cat_name', None)
            creator = self.request.get('creator', None)
            if function_type == "export": #if category to be exported is selected
                #category_query = db.GqlQuery('SELECT * FROM category WHERE name = \'%s\' AND creator = \'%s\'' %(cat_name, creator))
                xml='<?xml version="1.0" encoding="UTF-8"?>\n<site>\n'
                xml = xml + '</site>'
                self.response.headers['Content-Type']='text/xml; charset=utf-8'
                self.response.out.write(xml)
                
            all_categories = db.GqlQuery('SELECT * FROM category') #display all categories that the user can export
            template_values = {
                           'user' : user.nickname(),
                           'log_out_url' :  users.create_logout_url("/"),
                           'all_categories' : all_categories
                           }
            
            template = jinja_environment.get_template('exportcategory.html')
            self.response.out.write(template.render(template_values))
    
    
app = webapp2.WSGIApplication([('/export_category.*', ExportCategory)],
                              debug=True)

if __name__ == '__main__':
    pass