from google.appengine.ext import ndb
from users import MyUser
import itertools


class Anagram(ndb.Model):
    userKey = ndb.StringProperty()
    anagrams = ndb.StringProperty(repeated=True)

    def adding(self, word):
        user = MyUser().getCurrentUser()
        userid = user.user_id()
        o = ''.join(sorted(word.lower()))
        k = userid + o
        anagram = Anagram(id=k, userKey= userid, anagrams = word.lower().split(' '))
        anagram.put()

    def search(self, word):
        user = MyUser().getCurrentUser()
        userid = user.user_id()
        o = ''.join(sorted(word.lower()))
        k = userid + o
        anagram = ndb.Key('Anagram', k).get()
        return anagram

    def searchSub(self,word):
        user = MyUser().getCurrentUser()
        userid = user.user_id()

        o = ''.join(sorted(word.lower()))
        all_combinations = self.words(o)

        result = []
        searchArray = []
        for w in all_combinations:
            ss = ''.join(w)

            if len(w) > 2:
                n = ''.join(sorted(ss.lower()))
                if n not in searchArray:
                    searchArray.append(n)

        search = ndb.get_multi([ndb.Key('Anagram', userid + item) for item in searchArray])
        for s in search:
            if s is not None:
                result.extend(s.anagrams)

        return result

    def words(self, item):
        obj = [combination for i in range(len(item)+1) for combination in itertools.combinations(item, i)]
        return obj

    def upload_file(self,file):

        user = MyUser().getCurrentUser()
        userid = user.user_id()

        objects = file.split('\n')

        for i in objects:
            formatted_i = i.lower().strip('\r')
            x = ''.join(sorted(i.lower())).strip('\r')
            o = ndb.Key('Anagram', userid + x).get()


            if o is None:
                self.adding(formatted_i)
                MyUser().update_counter(3,1,1);
            elif (o is not None) or (formatted_i not in o.anagrams):
                o.anagrams.append(formatted_i)
                MyUser().update_counter(2,1,0);
            else:
                pass
