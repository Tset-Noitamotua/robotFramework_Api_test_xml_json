import sys, platform, os
sys.path.append(os.path.join('..', 'baseapi'))
import FileUpload, FileUploadLib
import threading, time
import Login
import RunThreadHandler


class MultiThreadLib(threading.Thread):
	def __init__(self,url,login_url):
		threading.Thread.__init__(self)
		self.url = url
		self.login = Login.Login(login_url)
		
		self.message = False
		self.keywords_withParams_List = []
		
	def thread_login(self,**login_kargs):
		self.login.user_login(**login_kargs)
		return 'user login succesfully'
		
	def build_user_threads(self,**kargs):
		'''
			kargs['users'] -> user list
			kargs['amount'] -> amount of requsts (send with same user)
			'''
		if len(kargs['users'])==1:
			for i in range(int(kargs['amount'])):
				exec "self.thead_%d = RunThreadHandler.RunThreadHandler(kargs['users'][0],self.url,sameUser=True)"%i
				# exec "self.thead_%d = self.run()"%i
				self.password = kargs['password']
				print 'thread %d is ready!'%i
		else:
			for user in kargs['users']:
				exec 'self.thead_%s = RunThreadHandler.RunThreadHandler(user,self.url)'%user
				exec 'self.thead_%s.set_login_time(kargs["time"])'%user
				print 'thread %s ready!'%user
		return 'Threads are ready by RunThreadHandler'
		
		
	def build_function(self, **kargs):
		'''function=upload_file_test	 fileId=${file_id }	crc=${file_crc}	fname=test.pdf	uploadPath=${common_upload_url}	'''
		function = kargs['function'].encode('utf-8') # function is like upload_file_test, which is keyword(lib functionname)
		for i in kargs: kargs[i]=kargs[i]#.encode('utf-8')
		self.keywords_withParams_List.append(kargs)
		print '{function: kargs} has been append in list'
		
		exec "self.thead_%s = RunThreadHandler.RunThreadHandler(user='whatever', url=self.url, **kargs)"%function
		print 'Thread self.thead_%s has been built'%function
		return len(self.keywords_withParams_List)
		
	def start_threads(self, **kargs): 
		'''
			kargs['users'] -> user list
			kargs['ms'] -> time duration 
			kargs['amount'] -> amount of requsts (send with same user)
			'''
		e = ''
		try:
			wait_for_responses = int(kargs['ms']) + 5000
			if len(kargs['users'])>1:
				start_time = time.time()
				self.start_users(kargs['users'])
				duration_time = time.time() - start_time
			else:
				login_kargs = {'username':kargs['users'][0]}
				login_kargs['password'] = self.password
				self.thread_login(**login_kargs)
				# self.login.user_login(**login_kargs)
				start_time = self.start_same_user(kargs['users'], kargs['amount'])
				time.sleep(wait_for_responses/1000)
				for i in range(int(kargs['amount'])):
					print '%s response message is '%i+eval('self.thead_%d.message'%i)
					if eval('self.thead_%d.message'%i) == 'INVALID_REQUEST':
						self.message = True
				duration_time = time.time() - start_time - wait_for_responses
				
				
			print '---multi threads finished---\n'
			print 'duration is '+str(duration_time)
			if duration_time > float(kargs['ms'])/1000:
				raise Exception('timeout for requests, need network and server assurance')
		
			if self.message:
				return 'got INVALID_REQUEST for exceed requests exception raised by Request Throttling'
			else:
				raise Exception('Expected exception not raised')
		except Exception, e:
			raise Exception(str(e))
			
	def start_same_user(self, users, amount):
		e = ''
		try:
			start_time = time.time()
			for i in range(int(amount)):
				exec 'self.thead_%d.start()'%i
				print '%s started - same user'%i
				
		except Exception,e:
			raise Exception(str(e))
		return start_time
			
	def start_users(self, users):
		for user in users:
			# exec 'self.thead_%s.set_login_time(self.time)'%user
			exec 'self.thead_%s.start()'%user
			print '%s started - users'%user
	
	def run_all_function_threads(self):
		try:
			for f in self.keywords_withParams_List:
				# exec 'self.thead_%s.setDaemon(True)'%f['function']
				exec 'self.thead_%s.start()'%f['function']
				print 'self.thead_%s.start()'%f['function']
				# time.sleep(1)
	
		except Exception,e:
			print e
		
	def clear_globalThreads(self):
		try:
			for f in self.keywords_withParams_List:
				# exec 'self.thead_%s.exit()'%f['function']
				exec 'del self.thead_%s'%f['function']
			return 'all global threads are deleted'
		except Exception,e:
			print e	