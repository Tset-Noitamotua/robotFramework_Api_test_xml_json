import threading, time
import RequestLib, CommonLib, MailLib, CalendarLib, ContactLib

class RunThreadHandler(threading.Thread):
	def __init__(self, **kargs):
		threading.Thread.__init__(self)
		print '-------------------------'
		print kargs
		self.url = kargs['url']
		self.runargs = kargs
		self.common = CommonLib.CommonLib(self.url)
		self.mail = MailLib.MailLib(self.url)
		
		self.functionVariable = False
		if kargs.has_key('function'):
			self.functionVariable = True
			
	def run(self):
		print 'run...............'
		if self.functionVariable:
			print 'need to call function'		
		else:
			self.msgheaderlist()
		
	def msgheaderlist(self):
		''' kargs['username'], kargs['password'] '''
		self.runargs['action'] = 'msgheaderlist'
		self.common.user_login(**self.runargs)
		self.common.request_send(eval('RequestLib.'+self.runargs['action']))
		
		