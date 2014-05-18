from google.appengine.ext import db

class Guest(db.Model):
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    email = db.StringProperty()
    custom1 = db.StringProperty()
    custom2 = db.StringProperty()
    note = db.StringProperty()
    attend = db.IntegerProperty()
    register_time = db.DateTimeProperty()
