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
        Populate()
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        
class Profile(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'profile.html')
        self.response.out.write(template.render( path, {} ) )

class VaccineList(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'vaccineList.html')
        self.response.out.write(template.render(path, template_values))

class DiseaseList(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'diseaseList.html')
        self.response.out.write(template.render(path, template_values))
        
class DiseaseMap(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'diseaseMap.html')
        self.response.out.write(template.render(path, template_values))

class JSONMeHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        results = db.GqlQuery("SELECT * FROM User WHERE userID = :1", users.get_current_user()).get()
        results = {"name" : results.name,
                   "dob" : self.changeDate(results.dob),
                   "email" : str(results.userID),
                   "clinic": results.clinic.address}
        self.response.out.write(json.dumps(results))
    
    def changeDate(self, date):
        date = str(date)
        date = date.split(" ")
        date = date[0].split("-")
        date = date[2]+"/"+date[1]+"/"+date[0]
        return date
        
VacList = []
class JSONVacHandler(webapp.RequestHandler):
    def get(self):
        vaccine = db.GqlQuery("SELECT * FROM VaccineTaken WHERE patient = :user ORDER BY dateExpired ASC",
                               user = users.get_current_user())
        response = self.makeJSON(vaccine)
        self.response.out.write(json.dumps(response))

    def makeJSON(self, response):
        jsonReady = []
        for vac in range(0,response.count()):
            VacList.append(response[vac].vaccine)
            jsonReady.append({"vaccine" : response[vac].vaccine.vaccine,"dateGiven" :  self.changeDate(response[vac].dateGiven),
                              "dateExpired" : self.changeDate(response[vac].dateExpired) })
        return jsonReady
    
    def changeDate(self, date):
        date = str(date)
        date = date.split(" ")
        date = date[0].split("-")
        date = date[2]+"/"+date[1]+"/"+date[0]
        return date

class JSONDisease (webapp.RequestHandler):
    def get(self):
        refList = list(set(VacList))
        disease =[]
        for vac in range(0,len(refList)):
            for dis in range(0,len(refList[vac].diseases)):
                key = str(refList[vac].diseases[dis])
                disease.append(db.GqlQuery("SELECT * FROM Disease WHERE __key__ = KEY(:1)", key).get()) 
        response = self.makeJSON(disease)
        self.response.out.write(json.dumps(response))
        
    def makeJSON(self, response):
        jsonReady = []
        for dis in range(0,len(response)):
            jsonReady.append(response[dis].disease)
        jsonReady = list(set(jsonReady))
        return jsonReady
    
class JSONMap (webapp.RequestHandler):
    def get(self):
        dis = self.request.get('disease')
        disease = db.GqlQuery("SELECT * FROM Disease WHERE disease = :1", dis)
        logging.info("RETURNED FROM STORE")
        logging.info(str(disease[0].country))
        self.response.out.write(json.dumps(disease[0].country))
        
    def makeJSON(self, response):
        jsonReady = []
        for dis in range(0,len(response[0].country)):
            jsonReady.append(response[0][dis])
        jsonReady = list(set(jsonReady))
        return jsonReady
        
class Populate():
    def __init__(self):
        logging.info("IN POPULATE")
        user = users.get_current_user()
        results = db.GqlQuery("SELECT * FROM User WHERE userID = :1", users.get_current_user()).get()
        if(results):
            logging.info("USER HAS LOGGED IN BEFORE")
        else:
            logging.info("NEW USER" + user.nickname())
            if(user == 'test@example.com'):
                self.generate()
                logging.info("This is the test user")
            else: 
                logging.info("This is a real user")
                self.generateRand()
        
    def generate(self):
        disease1 = Disease(disease= "Malaria", country=["IN","AF","LA","TH","KH","PG","VN","SD"])
        disease2 = Disease(disease= "Tetnus", country=["PK","AF","LA","SO","TD","NE","ML","CD"])
        disease3 = Disease(disease= "Yellow Fever", country=["PE","VE","EC","SN","LR","NG","CM","GA"])
        disease4 = Disease(disease= "Poliomyelitis", country=["BR","PE","VE","AR","MR","NE","NG","ML"])
        disease1.put()
        disease2.put()
        disease3.put()
        disease4.put()
       
        clin = Clinic(address="Henry Street, Dublin 1")
        clin.put()

        user = User(name="Mary Seery", userID=users.get_current_user(), dob=datetime.datetime(1990, 8, 17, 0, 0, 0), clinic=clin)
        user.put()
        
        drugs = ["Malarone", "Chloroquine", "Doxycycline", "Mefloquine"]
        for n in range(len(drugs)):
            vac = Vaccine(vaccine=drugs[n], diseases=[disease1.key(), disease2.key(), disease3.key(), disease4.key()])
            vac.put()
            vacTaken = VaccineTaken(patient=users.get_current_user(),
                    dateGiven=datetime.datetime(random.randint(2000, 2008), 8, 4, 12, 30, 45),
                    dateExpired=datetime.datetime(random.randint(2009, 2016), 8, 4, 12, 30, 45),
                    vaccine=vac)              
            vacTaken.put() 
            
    def generateRand(self):
        disease1 = Disease(disease= "Malaria", country=["IN","AF","LA","TH","KH","PG","VN","SD"])
        disease2 = Disease(disease= "Tetnus", country=["PK","AF","LA","SO","TD","NE","ML","CD"])
        disease3 = Disease(disease= "Hepatitis A", country=["RU","AF","LA","TH","PK","SA","YE","SY"])
        disease4 = Disease(disease= "Typhoid", country=["ID","MY","NP","IN","PH","PK","IR","AF"])
        disease1.put()
        disease2.put()
        disease3.put()
        disease4.put()
       
        clin = Clinic(address="Westmorland Street, Dublin 2")
        clin.put()

        user = User(name=users.get_current_user().nickname(), userID=users.get_current_user(), 
                    dob=datetime.datetime(random.randint(1960, 1990),random.randint(1, 12), random.randint(1, 28), 0, 0, 0),
                     clinic=clin, home='Ireland')
        user.put()
        
        drugs = ["Malarone", "TDaP", "Harix", "Vivotif Berna"]
        for n in range(len(drugs)):
            vac = Vaccine(vaccine=drugs[n], diseases=[disease1.key(), disease2.key(), disease4.key(), disease3.key()])
            vac.put()
            vacTaken = VaccineTaken(patient=users.get_current_user(),
                    dateGiven=datetime.datetime(random.randint(2000, 2008), 8, 4, 12, 30, 45),
                    dateExpired=datetime.datetime(random.randint(2009, 2016), 8, 4, 12, 30, 45),
                    vaccine=vac)              
            vacTaken.put() 


application = webapp.WSGIApplication([
  ('/POP', Populate),
  ('/', MainPage),
  ('/profile', Profile),
  ('/vaccine_list', VaccineList),
  ('/disease_list', DiseaseList),
  ('/disease_map', DiseaseMap),
  ('/json/map', JSONMap),
  ('/json/me', JSONMeHandler),
  ('/json/vaccines', JSONVacHandler),
  ('/json/diseases', JSONDisease)
], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main() 
