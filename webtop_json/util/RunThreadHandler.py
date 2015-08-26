import sys, platform, os
sys.path.append(os.path.join('..', 'baseapi'))
sys.path.append(os.path.join('..', 'testcase'))
import threading, time
import Login_sso
import Mail, FileUploadLib

class RunThreadHandler(threading.Thread):
	def __init__(self,user,url,sameUser=False,**kargs):
		threading.Thread.__init__(self)
		self.user = user
		self.sso = Login_sso.Login_sso(url)
		self.sameUser = sameUser
		self.message = 'OK'
		self.kargs=kargs
		self.mail = Mail.Mail(url)
		self.upload = FileUploadLib.FileUploadLib(url)
			
		
	def set_login_time(self, login_time):
		self.login_time = login_time
		
	
	def run(self):
		if self.kargs.has_key('function'):
			self.test_uploading(self.kargs)
		else:
			self.test_rateLimit()
				
	def test_rateLimit(self):
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
	
	def test_uploading(self,kargs):
		print '\n--------------------\n'
		print str(kargs)
		function = kargs['function']
		del kargs['function']
		exec 'self.upload.%s(**self.kargs)'%function
	
	