import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from model import Anagram
from users import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AddingPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            self.redirect('/')
            return

        template_values = {
            'logout_url': users.create_logout_url(''),
        }

        template = JINJA_ENVIRONMENT.get_template('Adding.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        word = self.request.get('anagram')
        data = Anagram().search(word)
        if data is not None:
            if word in data.anagrams:
                template_values = {
                    'logout_url': users.create_logout_url(''),
                    'error': True,
                    'message': 'Anagram already found in the system'
                }

                template = JINJA_ENVIRONMENT.get_template('Adding.html')
                self.response.write(template.render(template_values))
                return
            else:
                data.anagrams.append(word)
                data.put()
                MyUser().update_counter(1,1,0)
        else:
            Anagram().adding(word)
            MyUser().update_counter(3,1,1)

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'success': True,
            'message': 'Anagram added successfully'
        }

        template = JINJA_ENVIRONMENT.get_template('Adding.html')
        self.response.write(template.render(template_values))
