from google.appengine.ext import ndb
from google.appengine.api import users


class MyUser(ndb.Model):
    anagram_counter = ndb.IntegerProperty()
    words_counter = ndb.IntegerProperty()

    def getCurrentMyUser(self):
        user = users.get_current_myuser()
        return user

    def getUser(self, key):
        user = ndb.Key('MyUser', key).get()
        return user

    def adding(self, key):
        user = MyUser(id=key, anagram_counter = 0, words_counter = 0)
        user.put()

    def update_counter(self, type, word, anagram):
        user_key = self.getCurrentUser().user_id()
        user = self.getUser(user_key)

        if type == 1:
            if hasattr(user,'anagram_counter') == False or user.anagram_counter == None:
                user.anagram_counter = word
            else:
                user.anagram_counter = user.anagram_counter + word
        elif type == 2:
            if hasattr(user, 'words_counter') == False or user.words_counter == None:
                user.words_counter = word
            else:
                user.words_counter = user.words_counter + word
        else:
            if hasattr(user,'anagram_counter') == False or user.anagram_counter == None:
                user.anagram_counter = word
            else:
                user.anagram_counter = user.anagram_counter + word

            if hasattr(user, 'words_counter') == False or user.words_counter == None:
                user.words_counter = word
            else:
                user.words_counter = user.words_counter + word

        user.put()
