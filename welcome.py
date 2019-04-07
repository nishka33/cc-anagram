import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from adding import AddingPage
from mains import MainPage
from users import MyUser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('welcome.html')
            self.response.write(template.render(template_values))
            return
        else:
            myUser = MyUser().getUser(user.user_id())

            if myUser == None:
                MyUser().adding(user.user_id())

        self.redirect('/mains')



app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/mains', MainPage),
    ('/adding', AddingPage)
], debug=True)
