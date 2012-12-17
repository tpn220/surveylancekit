import webapp2
import jinja2
import os
import surveyusers
from google.appengine.api import users
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#The homepage display, where the user gets to select any of the given options

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            greeting = ("Welcome, %s!" %user.nickname())
            if not surveyusers.surveyuser.get_by_key_name(user.user_id()):
                new_user = surveyusers.surveyuser(key_name=user.user_id(), name=user.nickname())
                new_user.put()
            template_values = {
                               'user' : user.nickname(),
                               'log_out_url' : users.create_logout_url("/"),
                               }
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)

if __name__ == '__main__':
    pass