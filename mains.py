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

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            self.redirect('/')
            return



        myUser = MyUser().getUser(user.user_id())

        template_values = {
            'logout_url': users.create_logout_url(''),
            'words': myUser.words_counter,
            'anagrams': myUser.anagram_counter
        }

        template = JINJA_ENVIRONMENT.get_template('mains.html')
        self.response.write(template.render(template_values))

    def post(self):


         button = self.request.get('searchButton')

         if button == 'upload':
             f = self.request.get('file')
             Anagram().upload_file(f)
             user = user.get_current_user()
             myUser = MyUser().getUser(user.user_id())
             template_values = {
                 'logout_url': users.create_logout_url(''),
                 'words': myUser.words_counter,
                 'anagrams': myUser.anagram_counter,
                 'status': 'File upload successfully'
             }

             template = JINJA_ENVIRONMENT.get_template('mains.html')
             self.response.write(template.render(template_values))
             return

         word = self.request.get('search')
         data = []
         if button == 'search2':
             data = Anagram().searchSub(word)
         else:
             data = Anagram().search(word).anagrams

         template_values = {
             'logout_url': users.create_logout_url(''),
             'words': self.request.get('words'),
             'anagrams': self.request.get('anagrams'),
             'data': data
         }

         template = JINJA_ENVIRONMENT.get_template('mains.html')
         self.response.write(template.render(template_values))
