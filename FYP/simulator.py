import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import random
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from stored_info import *

class PersonGenerator:
    def generatePermanent(self):
        #for objects that are the basis of the system
        disease0 = Disease(disease= "Malaria", country=["IN","AF","LA","TH","KH","PG","VN","SD"])
        disease1 = Disease(disease= "Tetnus", country=["PK","AF","LA","SO","TD","NE","ML","CD"])
        disease2 = Disease(disease= "Hepatitis A", country=["RU","AF","LA","TH","PK","SA","YE","SY"])
        disease3 = Disease(disease= "Typhoid", country=["ID","MY","NP","IN","PH","PK","IR","AF"])
        disease4 = Disease(disease= "Yellow Fever", country=["PE","VE","EC","SN","LR","NG","CM","GA"])
        disease5 = Disease(disease= "Poliomyelitis", country=["BR","PE","VE","AR","MR","NE","NG","ML"])
        
        drugs = {"Malarone": disease0, "TDaP": disease1, "Harix": disease2, "Vivotif Berna": disease3, "Vf Vax": disease4, "Orimune Trivalent": disease5}
        for n in range(len(drugs)):
            vac = Vaccine(vaccine=drugs.keys()[n], diseases=drugs[vaccine].key())
            vac.put()
        
        clin1 = Clinic(address="Westmorland Street")
        clin2 = Clinic(address="Henry Street")
        clin3 = Clinic(address="Lombard Street")
        clin4 = Clinic(address="Wall Street")
        clin5 = Clinic(address="Orchard Street")
        clin1.put()
        clin2.put()
        clin3.put()
        clin4.put()
        clin5.put()
    
    def generateStatic(self):
        #for objects that use permanent objects
        firstNames = ["Louise","Michael","Jennifer", "David", "Karen", "Richard", "Michelle", "Betty", "Linda", "William", 
                      "Lisa", "John", "Dorothy", "Michael", "Robert", "Richard", "Richard", "Sandra", "Sarah", "Laura", "Robert"]
        lastNames = ["Sullivan", "Miller", "Reed", "Adams", "Price", "Ramirez", "Griffin", "Fisher", "Lee", "Gray ", 
                     "Anderson", "Bailey", "Hill", "Ellis", "Evans", "Baker", "Butler", "Harris", "Martin", " Murphy"]
        homeCountry = ["Ireland", "England", "America", "Australia", "New Zealand"]
        clinics = db.GqlQuery("SELECT * FROM Clinic")
        vaccines = db.GqlQuery("SELECT * FROM Clinic")
        
        for first in firstNames:
            for last in lastNames:
                
                user = User( name= first+" "+last, userID=first + last, 
                    dob=datetime.datetime(random.randint(1960, 1990),random.randint(1, 12), random.randint(1, 28), 0, 0, 0),
                     clinic=clinics[random.randint(0, clinics.count()-1)], home=homeCountry[random.randint(0, homeCountry.count()-1)],  
                     firstSession= datetime.datetime.today() - datetime.timedelta(days=random.randint(0, 90)), lastSession= datetime.datetime.today(), isActive = False)
                user.put()
                
                vacTaken = VaccineTaken(patient=user.userID,
                    dateGiven=datetime.datetime(random.randint(2000, 2008), random.randint(1, 12), random.randint(1, 28), 12, 30, 00),
                    dateExpired=datetime.datetime(random.randint(2009, 2016), random.randint(1, 12), random.randint(1, 28), 12, 30, 00),
                    vaccine=vac)              
                vacTaken.put() 
                
    
    def generateDynam(self):
        #adds session stuff for users
        