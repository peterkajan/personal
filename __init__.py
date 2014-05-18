from google.appengine.ext import ndb
from defines import * 

def exist(key):
    return key.get()

def existGuest( email ):
    key = ndb.Key(EmployeeEntity, email)
    return exist(key)
    
class Employee:
    firstname = ''
    lastname = ''
    email = ''
    employer = ''
    workplace = ''
    accomodation = 'no'
    residence = ''
    roommate = ''
    character = ''
    
class EmployeeEntity(ndb.Model):
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
        
def persistEmployee( empl ):
    #todo another email check 
    key = ndb.Key(EmployeeEntity, empl.email)    
    entity = EmployeeEntity(key=key)
    entity.set(empl)
    entity.put()
        
def createEmptyCharCnts():
    return [0 for i in range(len(characters))]

class Character(ndb.Model):
    cnt = ndb.IntegerProperty(default = 0)
    id = ndb.IntegerProperty()
    
    @classmethod
    def update(cls, id):
        char = cls.get_or_insert( str( id ))
        char.cnt += 1
        char.id = id
        char.put()
        
    @classmethod    
    def getCnts(cls):
        cnts = [0] * len(characters)
        for char in Character.query().fetch():
            cnts[char.id] = char.cnt
        
        return cnts;
#     
#     @classmethod
#     def createChars(cls):
#         chrs = Characters(cnts = createEmptyCharCnts())
#         chrs.put()
#         return chrs
# 
#     @classmethod
#     def update( cls, id ):   
#         chrs = cls.get()
#         chrs.cnts[id] += 1
#         chrs.put()
