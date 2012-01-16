import datetime

from google.appengine.ext import db
from google.appengine.api import users

class Clinic(db.Model):
    address = db.StringProperty()

class User(db.Model):
    userID = db.UserProperty()
    dob = db.DateTimeProperty()
    name = db.StringProperty()
    clinic = db.ReferenceProperty(Clinic)
    gender = db.BooleanProperty();
    
    def getGender(self):
        if(self.gender == true): 
            return "male"
        else:
             return "female"
    

class Vaccine(db.Model):
    """"Models an individual vaccine"""
    vaccine = db.StringProperty()
    diseases = db.ListProperty(db.Key)

    def getDiseases(self):
        return Disease.gql("WHERE vaccines = :1", self.key())

class VaccineTaken(db.Model):
  """Models an individual Vaccine event with a user."""
  patient = db.UserProperty()
  vaccine = db.ReferenceProperty(Vaccine) 
  dateGiven = db.DateTimeProperty()
  dateExpired = db.DateTimeProperty()


class Disease(db.Model):
    diseaseID = db.StringProperty()
    vaccines = db.ListProperty(db.Key)
    
    def diseases(self):
        return Vaccine.gql("WHERE disease = :1", self.key())