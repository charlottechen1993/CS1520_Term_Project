import webapp2
import models.userModel as userModel
from google.appengine.api import mail
import app_global
from webapp2_extras import sessions
import main
import time
    
    
# When webapp2 receives an HTTP GET request to the URL /, it instantiates the index class
# class index(webapp2.RequestHandler)
class index(main.index):
        
    #respond to HTTP GET requests
    def get(self):                                                  # /userFunctions
        user = app_global.unicode(self.session.get('user'))
        message = self.request.get('message')
        
        params = {
            'user': user,
            'user_id': self.session.get('user_id'),
            'message': message
        }
        
        userModel.getUsers()
        
        
        app_global.render_template(self, 'login.html', params)
  


class newUserSuccess(main.index):
    
    def get(self):
        params = {
            'user': app_global.unicode(self.session.get('user')),
            'user_id': app_global.unicode(self.session.get('user_id')),
            'email': app_global.unicode(self.session.get('email'))
            
        }
        app_global.render_template(self, 'newUserSuccess.html', params)
        
		  
		
        
#class userFunctions(webapp2.RequestHandler):
class userFunctions(main.index):
    def post(self):
        method = self.request.get('method')
        email = self.request.get('email').strip()   # unique identifier
        un = self.request.get('un').strip()         # name, identifier of person
        pw = self.request.get('pw').strip()
        pw2 = self.request.get('pw2').strip()
        gen = self.request.get('gender').strip()

        
        if method!='logout' and (email == '' or pw ==''):
            message = 'ERROR: You must fill out both email and password!'
            self.redirect('/user?message='+message)
            
        else:
            if method == 'newUser':                                 # /userFunctions?method=newUser
                #check that username does not already exist
                if len(userModel.getUser(email, pw)) > 0:
                    message = 'ERROR: Username already exist!'
                    self.redirect('/user?message='+message)
                elif pw != pw2:
                    message = 'ERROR: Passwords does not match each other'
                    self.redirect('/user?message='+message)
                else:
                    user_key = userModel.createNewUser(email, un, pw, gen)
                    mail.send_mail('admin@pittfashionshare.appspotmail.com', email, 'Registration', 'Thanks for registering with Pitt Fashion Share! Your account is now active.')
                    self.session['user'] = un
                    self.session['user_id'] = user_key.id()
                    self.session['pass'] = pw
                    self.session['email'] = email
                    self.session['gender'] = gen
         
                    self.redirect('/newUserSuccess')

                    
                    user = userModel.getUser(email, pw)
                    
                    # log newly registered user in
                    self.session['user'] = str(un),
                    self.session['email'] = str(email),
                    self.session['user_id'] = user_key.id()
                    self.session['imgURL'] = '/images/profile.jpg'
                    
                    params = {
                        'user': str(un),
                        'email': str(email)
                    }
                    
                    app_global.render_template(self, 'newUserSuccess.html', params)

                    self.redirect('/newUserSuccess')

  
            elif method == 'login':                                  # /userFunctions?method=login
                user = userModel.getUser(email, pw)
                
                if len(user) > 0:    # user login success
                    template = 'profile.html'
                    message = 'Logged in as ' + user[0].un
                    
                    self.session['email'] = user[0].email,
                    self.session['user'] = user[0].un,
                    self.session['user_id'] = user[0].user_id
                    self.session['description'] = user[0].description
                    self.session['gender'] = user[0].gender
                    self.session['pass'] = user[0].pw
                    print 'here'
                    print user[0].imgURL
                    if user[0].imgURL:
                        self.session['imgURL'] = user[0].imgURL
                    else:
                        self.session['imgURL'] = '/images/profile.jpg'
                    
                    self.redirect('/profile')
                else:
                    template = 'index.html'
                    message = 'ERROR: Login Fail!'
                    self.redirect('/user?message='+message)
            elif method == 'logout':                                   # /userFunctions?method=logout
                self.session['user'] = None
                self.session['user_id'] = None
                # redirect in ajax call in header.html
                
#        params = {
#            'message': message,
#            'user_id': self.session.get('user_id')
#        }        
#        
#
#        app_global.render_template(self, template, params)