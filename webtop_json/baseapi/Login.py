import requests, os, re, sys, platform
from Base import Base
sys.path.append(os.path.join('..', 'util'))
# from ImpLibs import consts

class Login(Base):
	def __init__(self, url):
		Base.__init__(self, url)

	def user_login(self,**kargs):
		#self.logger.debug('login*******************************')
		print 'Login: '+kargs['username']
		return self.request_send('LOGIN', **kargs)
		
	def user_logout(self):
		return self.request_send('LOGOUT')
		
	def user_auth_loginByToken(self, **kargs):
		response = self.post_to_r(**kargs)
		return response