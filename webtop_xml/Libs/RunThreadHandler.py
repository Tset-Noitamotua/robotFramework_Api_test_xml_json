import threading, time
import RequestLib, CommonLib, MailLib, CalendarLib, ContactLib

class RunThreadHandler(threading.Thread):
	def __init__(self, **kargs):
		self.url = kargs['url']
		self.runargs = kargs
		self.common = CommonLib.CommonLib(self.url)
		self.mail = MailLib.MailLib(self.url)
		
		threading.Thread.__init__(self)
	
	def run(self):
		''' kargs['username'], kargs['password'] '''
		self.runargs['action'] = 'msgheaderlist'
		self.common.user_login(**self.runargs)
		self.common.request_send(eval('RequestLib.'+self.runargs['action']))
		
		