import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import random
import logging

from stored_info import *

def generatePermanent():
        #for objects that are the basis of the system
        disease0 = Disease(disease="Malaria", country=["IN", "AF", "LA", "TH", "KH", "PG", "VN", "SD"]).put()
        disease1 = Disease(disease="Tetnus", country=["PK", "AF", "LA", "SO", "TD", "NE", "ML", "CD"]).put()
        disease2 = Disease(disease="Hepatitis A", country=["RU", "AF", "LA", "TH", "PK", "SA", "YE", "SY"]).put()
        disease3 = Disease(disease="Typhoid", country=["ID", "MY", "NP", "IN", "PH", "PK", "IR", "AF"]).put()
        disease4 = Disease(disease="Yellow Fever", country=["PE", "VE", "EC", "SN", "LR", "NG", "CM", "GA"]).put()
        disease5 = Disease(disease="Poliomyelitis", country=["BR", "PE", "VE", "AR", "MR", "NE", "NG", "ML"]).put()
        
        drugs = {"Malarone": disease0, "TDaP": disease1, "Harix": disease2, "Vivotif Berna": disease3, 
                 "Vf Vax": disease4, "Orimune Trivalent": disease5}
        for n in range(len(drugs)):
            vacName = drugs.keys()[n]
            Vaccine(vaccine= vacName, diseases=[drugs[vacName]])
        
        Clinic(address="Westmorland Street").put()
        Clinic(address="Henry Street").put()
        Clinic(address="Lombard Street").put()
        Clinic(address="Wall Street").put()
        Clinic(address="Orchard Street").put()

        
        Emergency(country="BN", police= "993", ambulance="991", fire="995").put()
        Emergency(country="KH", police= "117", ambulance="119", fire="118").put()
        Emergency(country="TL", police= "112", ambulance="112", fire="112").put()
        Emergency(country="ID", police= "110", ambulance="118", fire="113").put()
        Emergency(country="LA", police= "02", ambulance="03", fire="01").put()
        Emergency(country="MY", police= "994", ambulance="999", fire="994").put()
        Emergency(country="MM", police= "119", ambulance="119", fire="199").put()
        Emergency(country="PH", police= "117", ambulance="117", fire="117").put()
        Emergency(country="SG", police= "999", ambulance="995", fire="995").put()
        Emergency(country="TH", police= "191", ambulance="1669", fire="199").put()
        Emergency(country="VN", police= "113", ambulance="115", fire="114").put()
        Emergency(country="IN", police= "100", ambulance="102", fire="101").put()

    
def generateStatic():
        #for objects that use permanent objects
        firstNames = ["Louise", "Michael", "Jennifer", "David", "Karen"]#, "Richard", "Michelle", "Betty", "Linda", "William",
                      #"Lisa", "John", "Dorothy", "Michael", "Robert", "Richard", "Richard", "Sandra", "Sarah", "Laura", "Robert"]
        lastNames = ["Sullivan", "Miller", "Reed", "Adams", "Price"]#, "Ramirez", "Griffin", "Fisher", "Lee", "Gray ",
                     #"Anderson", "Bailey", "Hill", "Ellis", "Evans", "Baker", "Butler", "Harris", "Martin", " Murphy"]
        homeCountry = ["Ireland", "England", "America", "Australia", "New Zealand"]
        clinics = db.GqlQuery("SELECT * FROM Clinic")
        vaccines = db.GqlQuery("SELECT * FROM Vaccine")
        
        for first in firstNames:
            for last in lastNames:
                
                user = User(name=first + " " + last, userID=users.User(first + last),
                    dob=datetime.datetime(random.randint(1960, 1990), random.randint(1, 12), random.randint(1, 28), 0, 0, 0),
                     clinic=clinics[random.randint(0, clinics.count() - 1)], home=homeCountry[random.randint(0, len(homeCountry) - 1)],
                     firstSession=datetime.datetime.today() - datetime.timedelta(days=random.randint(0, 90)), 
                     lastSession=datetime.datetime.today(), isActive=False)
                user.put()
                for num in range(0, 3):
                    logging.info(str(vaccines[num]))
                    VaccineTaken(patient=user.userID,
                                            dateGiven=datetime.datetime(random.randint(2004, 2008), random.randint(1, 12), random.randint(1, 28), 12, 30, 00),
                                            dateExpired=datetime.datetime(random.randint(2012, 2016), random.randint(1, 12), random.randint(1, 28), 12, 30, 00),
                                            vaccine=vaccines[num]).put() 
                
    
def generateDynam():
        #adds session stuff for users
        countries = ["BN", "KH", "TL", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "VN", "IN"]
        users = db.GqlQuery("SELECT * FROM User")
        logging.info(users.count())
        for user in range(0, users.count()):
            start = datetime.datetime(2011, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), 30, 00)
            sess = Sessions(userID=users[user].userID, sessionStart= start,
                            sessionEnd=start + datetime.timedelta(minutes=random.randint(0, 90)), country=countries[random.randint(0, len(countries)-1)])
            sess.put()

