import datetime

from google.appengine.ext import db
from google.appengine.api import users

"""STATIC CLASSES: POPULATED ONLY ONCE"""

class Clinic(db.Model):
    address = db.StringProperty()

class Disease(db.Model):
    disease = db.StringProperty()
    country = db.StringListProperty()

class Vaccine(db.Model):
    """"Models an individual vaccine"""
    vaccine = db.StringProperty()
    diseases = db.ListProperty(db.Key)

"""ACTIVE CLASSES, NEED TO BE POPULATED PER USER LOG IN"""

class User(db.Model):
    userID = db.UserProperty()
    dob = db.DateTimeProperty()
    name = db.StringProperty()
    home = db.StringProperty()
    clinic = db.ReferenceProperty(Clinic)
    firstSession = db.DateTimeProperty()
    
    lastSession = db.DateTimeProperty()
    isActive = db.BooleanProperty()
    
class VaccineTaken(db.Model):
  """Models an individual Vaccine event with a user."""
  patient = db.UserProperty()
  vaccine = db.ReferenceProperty(Vaccine) 
  dateGiven = db.DateTimeProperty()
  dateExpired = db.DateTimeProperty()
  
class Sessions(db.Model):
    userID = db.UserProperty()
    sessionStart = db.DateTimeProperty()
    sessionEnd = db.DateTimeProperty()
    country = db.StringProperty()
    
    
