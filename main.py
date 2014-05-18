import defines
from django.conf import settings
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from utils import BaseHandler, sessionConfig
import logging
import os
import webapp2
from model import Guest, persistTestGuests
from google.appengine.ext import ndb
from google.appengine.runtime import DeadlineExceededError
from django.template.loader import render_to_string
from urllib import urlencode


if not settings.configured:
    settings.configure()
settings.USE_I18N = False
settings.TEMPLATE_DIRS = ('.')
settings.TEMPLATE_DEBUG = True

URL_MAIN='/'
URL_CONFIRMATION_ACCEPT='/potvdrdenie'
URL_CONFIRMATION_REJECT='/jenamtoluto'
URL_ACCEPT='/accept'
URL_REJECT='/reject'

#admin interface
URL_PAGE_SENDER='/send_mails_secret'
URL_PAGE_TEST_DATA_IMPORT='/import_secret'
    
def render_template(response, template_file, template_values):
    response.out.write( render_to_string(template_file, template_values))    

def _getKey(handler):
    key = None
    keyUrl = handler.request.get('key')
#     if not keyUrl:
#         keyUrl = handler.session.get('key')
        
    if keyUrl:
        try:
            key = ndb.Key( urlsafe = keyUrl )
            handler.session['key'] = key.urlsafe()
        except (BaseException):
            logging.exception('Failed to create key: %s', keyUrl)    
    else:
        logging.info('No key in url or session')
    
    return key

def _getGuest(handler, key):
    guest = None
    try:
        guest = key.get()
        if not guest:
            logging.error('Guest is None, key: %s', key.urlsafe())
        
    except (BaseException):
        logging.exception('Failed to get guest, key: %s', key.urlsafe())
        
    return guest
    
    
class MainHandler(BaseHandler):

    def displayPage(self, **kwargs):
        render_template(self.response, 'main.html', kwargs)
        
    def displayAnonymPage(self, **kwargs):
        render_template(self.response, 'anonym.html', kwargs)
        
    def get(self):
        key = _getKey(self)
        if not key:
            return self.displayAnonymPage()
        
        guest = _getGuest(self, key)
        if not guest:
            return self.displayAnonymPage()
        
        logging.info('GET guest: ' + unicode(guest.firstname) 
            + ' ' + unicode(guest.lastname  + ' ' + guest.email))   
        
        return self.displayPage( 
            firstname=guest.firstname,
            accept_link=URL_ACCEPT + '?' + urlencode({'key': key.urlsafe()}), 
            reject_link=URL_REJECT + '?' + urlencode({'key': key.urlsafe()}),
        )  


class AcceptHandler(BaseHandler):            
    def get(self):
        key = _getKey(self)
        guest = _getGuest(self, key)
        guest.attend = 1
        guest.put()
        sendConfirmationMail(guest)
        return self.redirect(URL_CONFIRMATION_ACCEPT)
        
        
class RejectHandler(BaseHandler):
    def get(self):
        key = _getKey(self)
        guest = _getGuest(self, key)
        guest.attend = 0
        guest.put()
        if defines.MAIL_REJECTION:
            sendRejectionMail(guest, generateLink(guest))
        return self.redirect(URL_CONFIRMATION_REJECT)

        
class ConfirmationAcceptHandlar(BaseHandler):
    def get(self):
        render_template(self.response, 'confirmationAccept.html', {})
        
        
class ConfirmationRejectHandlar(BaseHandler):
    def get(self):
        render_template(self.response, 'confirmationReject.html', {})
                         

class SenderPage(BaseHandler):
    def get(self):
        out = '\n'
        links = []
        for guest in Guest.query().fetch():
            link = generateLink(guest)
            out += unicode( guest.firstname ) + ' ' + unicode( guest.lastname ) + '\n' + \
                    ' ' + link + '\n';
            #sendInvitationMail(guest, link)
            links.append((guest.firstname, guest.lastname, guest.email, link))       
            
        logging.info('Links:\n' + out);
        logging.info('Links machine:\n%s', links);
        _sendMail(defines.MAIL_FROM, 'peto.kajan@gmail.com', 'Links', unicode(links))
        self.abort(404)                  
        
def generateLink(guest):
    return defines.DOMAIN + '?key=' + guest.key.urlsafe()

def _sendMail(senderAddress, userAddress, subject, body):
    try:
        mail.send_mail(senderAddress, userAddress, subject, body)
    except (Exception, DeadlineExceededError):
        logging.exception('Failed to send email %s ', userAddress) 
            
def sendInvitationMail(guest, link):
    logging.info('Sending invitation mail sent to %s', guest.email)
    userAddress = guest.email
    senderAddress = defines.MAIL_FROM
    subject = defines.MAIL_INVITATION_SUBJECT
    body = defines.MAIL_INVITATION_TEXT.format(name=guest.firstname, link=link)
    _sendMail(senderAddress, userAddress, subject, body)
    logging.info('Invitation mail sent successfully')
    
def sendConfirmationMail(guest):
    logging.info('Sending confirmation mail to %s', guest.email)
    userAddress = guest.email
    senderAddress = defines.MAIL_FROM
    subject = defines.MAIL_CONFIRMATION_SUBJECT
    body = defines.MAIL_CONFIRMATION_TEXT.format(name=guest.firstname,)
    _sendMail(senderAddress, userAddress, subject, body)
    logging.info('Confirmation mail sent successfully')
    
def sendRejectionMail(guest, link):
    logging.info('Sending rejection mail to %s', guest.email)
    userAddress = guest.email
    senderAddress = defines.MAIL_FROM
    subject = defines.MAIL_REJECTION_SUBJECT
    body = defines.MAIL_REJECTION_TEXT.format(name=guest.firstname, link=link)
    _sendMail(senderAddress, userAddress, subject, body)
    logging.info('Rejection mail sent successfully')
    
class TestDataImportPage(BaseHandler):
    def get(self):
        persistTestGuests()
        self.abort(404)

    
pages = [
    (URL_MAIN, MainHandler),
    (URL_CONFIRMATION_ACCEPT, ConfirmationAcceptHandlar),
    (URL_CONFIRMATION_REJECT, ConfirmationRejectHandlar),
    (URL_ACCEPT, AcceptHandler),
    (URL_REJECT, RejectHandler),
    (URL_PAGE_SENDER, SenderPage),
    (URL_PAGE_TEST_DATA_IMPORT, TestDataImportPage)]
    
application = webapp2.WSGIApplication(pages, config = sessionConfig)

def main():
    # Set the logging level in the main function
    # See the section on Requests and App Caching for information on how
    # App Engine reuses your request handlers when you specify a main function
    logging.getLogger().setLevel(logging.INFO)
    

if __name__ == '__main__':
    main()