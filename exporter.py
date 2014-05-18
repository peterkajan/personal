from google.appengine.ext import db
from google.appengine.tools import bulkloader
from google.appengine.ext import ndb

class Employee(db.Model):
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    email = db.StringProperty()
    employer = db.StringProperty()
    workplace = db.StringProperty()
    accomodation = db.StringProperty()
    residence = db.StringProperty()
    roommate = db.StringProperty()


def toUtf8( str ):
    if (str):
        return str.encode('utf-8')
    else:
        return None
    
class AlbumExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Employee',
                                    [('firstname', toUtf8, ''),
                                     ('lastname', toUtf8, ''),
                                     ('email', toUtf8, ''),
                                     ('employer', toUtf8, ''),
                                     ('workplace', toUtf8, ''),
                                     ('accomodation', toUtf8, ''),
                                     ('residence', toUtf8, ''),
                                     ('roommate', toUtf8, ''),
                                    ])


exporters = [AlbumExporter]