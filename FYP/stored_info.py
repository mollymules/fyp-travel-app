import datetime

from google.appengine.ext import db
from google.appengine.api import users

class Clinic(db.Model):
    address = db.StringProperty()

class User(db.Model):
    userID = db.UserProperty()
    dob = db.DateTimeProperty()
    name = db.StringProperty()
    home = db.StringProperty()
    clinic = db.ReferenceProperty(Clinic)
    
class Disease(db.Model):
    disease = db.StringProperty()
    country = db.StringListProperty()
    
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

