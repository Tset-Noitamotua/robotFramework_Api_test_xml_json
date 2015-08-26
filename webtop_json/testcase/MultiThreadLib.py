import threading, time
import RequestLib, CommonLib, RunThreadHandler, MailLib, CalendarLib, ContactLib

class MultiThreadLib():
	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)
		self.mail = MailLib.MailLib(self.url)
		
	def build_multithread(self, username, domain, password, amount): # moved from old
		self.usernameL = []
		for i in range(int(amount)):
			self.usernameL.append(username+str(i+1))
	
		kargs = {}
		kargs['url'] = self.url
		kargs['password'] = password
		for user in self.usernameL:
			kargs['username'] = user + domain
			exec 'self.thead_%s = RunThreadHandler.RunThreadHandler(**kargs)'%user
		
	def build_multithreads(self, *args):
		'''upload_file_test	fileId=${file_id }	crc=${file_crc}	fname=test.pdf	uploadPath=${common_upload_url}	'''
		argsL = []
		for i in args:
			argsL.append(i)
		return argsL
	
		
	def start_threads(self, **kargs): 
		start_time = time.time()
		e = ''
		try:
			for user in self.usernameL:
				exec 'self.thead_%s.start()'%user
			duration_time = time.time() - start_time
			print 'duration is '+str(duration_time)
			if duration_time > float(kargs['ms'])/1000:
				raise Exception('timeout for requests, need network and server assurance')
		except Exception, e:
			if 'INVALID_REQUEST' in e.message: # expect the correct exception when exceed
				return 'got INVALID_REQUEST for exceed requests exception raised by Request Throttling' # exceed request mount
			else:
				e = 'Wrong exception: '+e
		if not e:
			raise Exception('No any exception raised')
		elif 'Wrong exception' in e:
			raise Exception('Need INVALID_REQUEST for exceed requests exception raised by Request Throttling')
		
		