import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import random
import logging
import simplejson as json

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from stored_info import *

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
class VaccineList(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        """vaccines_taken = db.GqlQuery("SELECT * FROM VaccineTaken WHERE patient = :1", user)        
        template_values = {
            'user': user,
            'vaccines': vaccines_taken,
        }"""
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'vaccineList.html')
        self.response.out.write(template.render(path, template_values))
        
        
class DiseaseList(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        """vaccines = db.GqlQuery("SELECT * FROM VaccineTaken WHERE patient = :1", user) 
        for vac in vaccines:
            diseases = db.GqlQuery("SELECT diseases FROM Vaccine WHERE vaccine = :1", vac)       
        template_values = {
            'user': user,
            'diseases': diseases,
        }
        self.response.out.write(template.render(path, template_values))"""
        path = os.path.join(os.path.dirname(__file__), 'diseaseList.html')
        
class Profile(webapp.RequestHandler):
    def get(self):
        logging.info("In the profile method")
        path = os.path.join(os.path.dirname(__file__), 'profile.html')
        self.response.out.write(template.render( path, {} ) )
    
class JSONMeHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        """userStat = db.GqlQuery("SELECT name FROM User WHERE userID = :1", user)"""
        userStat = {"name" : "MAry",
                   "dob" : "12433",
                   "email" : "fdfsf@dmsa",
                   "clinic": "djfndsf"}
        self.response.out.write(json.dumps(userStat))
        
class JSONVacHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        vaccine = db.GqlQuery("SELECT * FROM VaccineTaken WHERE patient = :1", user)
        """ response = {"vaccine" :[
                   {"dob" : userStat.dob},
                   "email" : user,
                   "clinic": userStat.clinic]}"""
        logging.info(json.dumps(vaccine))
        self.response.out.write(json.dumps(vaccine))
        

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/profile', Profile),
  ('/vaccine_list', VaccineList),
  ('/disease_list', DiseaseList),
  ('/json/me', JSONMeHandler),
  ('/json/vaccines', JSONVacHandler),
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

def populate():
        drugs = ["Malarone", "Chloroquine", "Doxycycline", "Mefloquine", "Primaquine"]
        for n in range(len(drugs)):
            vac = Vaccine(vaccine=drugs[n])
            vac.put()
            vacTaken = VaccineTaken(patient=users.get_current_user(),
                       dateGiven=datetime.datetime(random.randint(2000, 2008), 8, 4, 12, 30, 45),
                       dateExpired=datetime.datetime(random.randint(2009, 2016), 8, 4, 12, 30, 45),
                       vaccine=db.get(drugs[n]))              
            vacTaken.put()
        user = User(name="Mary Seery", userID=users.get_current_user(), dob=datetime.datetime(1990, 8, 17, 0, 0, 0),
                gender=false, clinic=Clinic(address="Westmorland Street, Dublin 2"))
        user.put()   
