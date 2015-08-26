import sys, platform, os
sys.path.append(os.path.join('..', 'baseapi'))
import threading, time
import Login_sso
import Mail

class RunThreadHandler(threading.Thread):
	def __init__(self,user,url,sameUser=False):
		threading.Thread.__init__(self)
		self.user = user
		self.sso = Login_sso.Login_sso(url)
		self.mail = Mail.Mail(url)
		self.sameUser = sameUser
		self.message = 'OK'
		
	def set_login_time(self, login_time):
		self.login_time = login_time
	
	def run(self):
		e = ''
		try:
			if not self.sameUser:
				print '%s start run'%self.user
				# kargs = {'username':self.user}
				# kargs['time'] = self.login_time
				# self.sso.sso_login(**kargs)
			kargs = {'params.folderPath':'INBOX'}
			self.mail.list_mail(**kargs)
		except Exception, e:
			if 'INVALID_REQUEST' in e.message: # expect the correct exception when exceed
				self.message = 'INVALID_REQUEST'
				# return 'got invalid request'
				# # raise Exception('got INVALID_REQUEST') # exceed request mount
				
		