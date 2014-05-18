from google.appengine.ext import ndb

def exist(key):
    return key.get()

def existGuest( email ):
    key = ndb.Key(Guest, email)
    return exist(key)

    
class Guest(ndb.Model):
    firstname = ndb.StringProperty(required = True)
    lastname = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    employer = ndb.StringProperty(required = True)
    workplace = ndb.StringProperty(required = True)
    accomodation = ndb.StringProperty()
    residence = ndb.StringProperty()
    roommate = ndb.StringProperty()
    character = ndb.StringProperty(required = True)
    
    def set(self, emp):
        self.firstname      = emp.firstname   
        self.lastname       = emp.lastname    
        self.email          = emp.email       
        self.employer       = emp.employer    
        self.workplace      = emp.workplace   
        self.accomodation   = emp.accomodation
        self.residence      = emp.residence   
        self.roommate       = emp.roommate    
        self.character      = emp.character   
        
def persistGuest( empl ):
    #todo another email check 
    key = ndb.Key(Guest, empl.email)    
    entity = Guest(key=key)
    entity.set(empl)
    entity.put()
