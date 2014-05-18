# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import datetime

def exist(key):
    return key.get()

    
class Guest(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.StringProperty()
    custom1 = ndb.StringProperty()
    custom2 = ndb.StringProperty()
    note = ndb.StringProperty()
    attend = ndb.IntegerProperty()
    register_time = ndb.DateTimeProperty()
    
    def put(self, *args, **kwargs):
        if not kwargs.pop('no_update_time', None):
            self.register_time = datetime.datetime.utcnow()
        return super(Guest, self).put(*args, **kwargs)
        


def persistTestGuests():
    for i in range(10):
        g = Guest()
        g.firstname = 'Jožko{}'.format(i)
        g.lastname = 'Mrkvička{}'.format(i)
        g.email = 'jozko{}@geustflow.sk'.format(i)
        g.put(no_update_time=True)