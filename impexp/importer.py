from google.appengine.ext import db
from google.appengine.tools import bulkloader
from model import Guest

def fromUtf8( string ):
    return string.decode('utf-8')
    

class GuestLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Guest',
                                   [('firstname', fromUtf8),
                                    ('lastname', fromUtf8),
                                    ('email', str)
                                   ])

loaders = [GuestLoader]