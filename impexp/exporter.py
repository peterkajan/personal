from google.appengine.tools import bulkloader
from model import Guest

def toUtf8( string ):
    if (string):
        return string.encode('utf-8')
    else:
        return None
        
class AlbumExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'Guest',
                                    [('firstname', toUtf8, ''),
                                     ('lastname', toUtf8, ''),
                                     ('email', toUtf8, ''),
                                     ('custom1', toUtf8, ''),
                                     ('custom2', toUtf8, ''),
                                     ('note', toUtf8, ''),
                                     ('attend', str, ''),
                                    ])

exporters = [AlbumExporter]