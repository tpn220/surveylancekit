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

class ExportCategory(webapp2.RequestHandler):
    
    def get(self):       
        user = users.get_current_user()
          
        if user:
            function_type = self.request.get('function', None)
            
            if function_type == "export":
                root = ET.Element('root')
                child = ET.Element('child')
                root.append(child)
                child.attrib['name'] = "Charlie"
                file = open("test.xml", 'w')
                ET.ElementTree(root).write(file)
                file.close() 
                
            all_categories = db.GqlQuery('SELECT * FROM category')
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