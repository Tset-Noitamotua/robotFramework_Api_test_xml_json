import time, datetime, os, random, re, copy, sys, urllib, Upload
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder, TestCodeException, msgconsts
from Contact import Contact
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 

class GlobalHelper():
	def __init__(self):
		pass
		
	def split_for_str_by_char(self, **kargs):
		wholeStr = kargs['str']
		char = kargs['char']
		index = int(kargs['index'])
		return wholeStr.split('/')[index]
		
	def create_object_list(self, *kargs):
		list = []
		for i in kargs:
			list.append(eval(i))
		return list
		
	def create_utf8_list(self, *kargs):
		list = []
		for i in kargs:
			list.append(i.encode('utf-8'))
		return list
		
	def create_int_list(self, *kargs):
		return [int(i) for i in kargs]
		
	def create_big_hash(self, **kargs):
		big_hash = {}
		for key in kargs:
			big_hash[key] = kargs[key]
		return big_hash
		
	def get_res_value_by_key(self, **kargs):
		''' This is used for get hash value from result, i.e.  "result" : {
				"http://fepmsshost:5229/calendars/webtop5@openwave.com/webtop_14c2c35243e" : 'blabla'
			 } '''
		if type(kargs['res']) in [str, unicode] : hash = eval(kargs['res'])
		else:  hash = kargs['res']
		key = kargs['key']
		return hash[key]
		
	def get_id_list_by_name(self, **kargs):
		'''
		input: name - get by "name" : "Default", ..
			   expectCnt - expect number of addressbook
			   res - list addressbook response string
		output: exception or matched addressbook ids list(all=True, or if has kargs['index'], return matched id)
		'''
		all = False
		name = ''
		if kargs.has_key('all'): all = True
		if kargs.has_key('name'): name = kargs['name']
		result_list = utils.getIdListByName(name, kargs['res'], all=all)
		if kargs.has_key('expectCnt'):
			expectCnt = int(kargs['expectCnt'])
			if len(result_list) != expectCnt:
				raise Exception('Expect count is %s, but actually got %s'%(expectCnt, len(result_list)))
			print 'Count checked!'
		if kargs.has_key('index'):
			index = int(kargs['index'])
			return result_list[index]
		return result_list
		
	def expect_results_cnt_from_res(self, **kargs):
		''' res=${report_event2}	cnt=5 
			kargs['middle_key'] -> json key in middle layer between 'result' and 'results'. i.e."events"  '''
		if type(kargs['res']) in [str, unicode] : hash = eval(kargs['res'])
		else:  hash = kargs['res']
		if kargs.has_key('middle_key'):
			results_list = hash[kargs['middle_key']]
		else:
			results_list = hash['result']
		if not len(results_list) == int(kargs['cnt']):
			raise Exception('Expect %s from result-results but got %s'%(kargs['cnt'], len(results_list)))
		return 'cnt is correct'
		
	# def check_created_id_by_name(self, **kargs):
		# '''
		# input : name - contact group name
				# addressbook_id
				# expectCnt - expect number of addressbook
		# description : check if the contact group is right
		
		# '''
		# result_id = utils.getCreatedIdFromRes(**kargs)
		# return result_id
		
	def check_result_item(self, **kargs):
		''' kargs['res'] comes from "result" hash in response;
			the only other arg is the hash to check, values has to be separated by SPACE
				like: emails=${common_from}${common_domain} ${common_to}${common_domain}
			'''
		if not type(kargs['res']) == dict:
			result = eval(kargs['res'])
		else: result = kargs['res']
			
		del kargs['res']
		item = kargs.keys()[0] # the item name to check (get from kargs name)
		expect_list = kargs[item].split(' ') # the expect value list (get from kargs value)
		notFound = ''
		for expect_result in expect_list:
			if not str(expect_result) in str(result[item]):
				notFound = notFound + expect_result + ' '
		if notFound:
			raise Exception('Not found [%s] from response'%notFound)
		return 'All values checked'
		
	def check_result_items(self, **kargs):
		'''	kargs['res']
			i.e. res=${read_event}	calendarId=${cal id}	summary=singleEvent_${startTime}	'''
		if not type(kargs['res']) is dict: result_hash = eval(kargs['res'])
		else: result_hash = kargs['res']
		del kargs['res']
		failed = []
		for exp_k in kargs:
			if result_hash.has_key(exp_k):
				if type(kargs[exp_k]) == dict:
					if exp_k == 'recurrence' and kargs['recurrence'].has_key('until'): # if has recurrenct['until']: until in request is str but response is long type
						if not (str(kargs[exp_k]['until'])==str(result_hash[exp_k]['until'])): # until: request is str but response is long type
							failed.append('until not same')
						del kargs['recurrence']['until'], result_hash['recurrence']['until']
					if not cmp(kargs[exp_k], result_hash[exp_k]) == 0:
						failed.append('Not found dict value: %s -got %s'%(str(kargs[exp_k]),  result_hash[exp_k] ))
				else:
					if not str(kargs[exp_k]).lower() == str(result_hash[exp_k]).lower():
						failed.append('Not found str value: '+ str(kargs[exp_k]))
			else:
				failed.append('Not found key: '+str(exp_k))
		if failed:
			raise Exception(str(failed))
		return 'All checked'
		
	def check_hash_params_From_list(self, **kargs):
		'''kargs['list'] -> a list contain some hash, eg.:
				"result" : [ {
				"id" : "http://msscalpab:5229/calendars/webtop8@openwave.com/6921258140085803885-webtop_14bc98884c8",
				"name" : "delTest",
				"color" : null,
				"visible" : true,
				"primary" : false,
				"personal" : true,
				"readOnly" : false,
				"sharingUrl" : "http://proxyHost:1234/calendars/webtop8@openwave.com/6921258140085803885-webtop_14bc98884c8"
			  }, {
				"id" : "http://msscalpab:5229/calendars/webtop8@openwave.com/6921258140085803885-webtop_14bc98e0f4e",
				"name" : "newName",
				"color" : null,
				"visible" : true,
				"primary" : false,
				"personal" : true,
				"readOnly" : false,
				"sharingUrl" : "http://proxyHost:1234/calendars/webtop8@openwave.com/6921258140085803885-webtop_14bc98e0f4e"
			  }]
		other kargs: key1=value1 key2=value2 -> check the pair of key/value from ONLY one hash, eg:
			name=newName id=...0085803885-webtop_14bc98e0f4e
			'''
		if type(kargs['list']) in [str, unicode] : list = eval(kargs['list'])
		else:  list = kargs['list']
		del kargs['list']
		exp_items = kargs.items()
		found = False
		for list_hash in list:
			pop_list = []
			for hash in list_hash: 
				if not type(list_hash[hash]) in [str, unicode]: pop_list.append(hash)
			for pop in pop_list: 
				list_hash.pop(pop)
			
			list_items = list_hash.items()
			if set(exp_items).issubset(set(list_items)): found = True
		
		if not found:
			raise Exception('Not any matched found')
		return str(exp_items)+' is matched from list'
	
	# def get_hash_params_From_list(self, **kargs):
		# list = eval(kargs['list'])
		# del kargs['list']
		
	def get_list_value(self, **kargs):
		'''	kargs['list'] is a list
			kargs['index'] start from 0'''
		list = kargs['list']
		index = int(kargs['index'])
		return list[index]
		
	def check_list_cnt(self, **kargs):
		if not type(kargs['list']) == list: 
			l = eval(kargs['list'])
		else: l= kargs['list']
		
		if not len(l) == int(kargs['exp_cnt']):
			raise Exception('expect %s but found %s'%(int(kargs['exp_cnt']), len(l)))
		else: 
			return 'Count is matched'
		
	def check_listString_from_res(self, **kargs):
		list = kargs['exp_list'].split()
		failed = ''
		for exp in list:
			if exp not in kargs['res']:
				failed = failed + exp + ', '
		if failed:
			raise Exception('Not found: '+failed)
		return 'All checked from download'
		
		
		
		
	def makeHashField(self, **kargs):
		'''int-startMillis=${startTime}000	str-summary=singleEvent${startTime}'''
		hash={}
		for k in kargs:
			if 'int-' in k: # i.e. '1234567890'
				name = k.replace('int-', '')
				hash[name] = int(kargs[k])
			elif 'list-' in k or 'bool-' in k or 'eval-' in k: # i.e. '[123,456]'
				name = '-'.join(k.split('-')[1:]) # k.split('-')[1]
				hash[name] = eval(kargs[k])
			elif 'dict-' in k: # i.e. "{'a':1,'b':2}"
				name = k.replace('dict-', '')
				hash[name] = kargs[k]
			elif 'str-' in k: # i.e. 'abcdef'
				name = k.replace('str-', '').encode('utf-8')
				hash[name] = str(kargs[k]).encode('utf-8')
			else:  # i.e. [1,2,3,'a','b','c']
				hash[k] = kargs[k]
				
				
		if kargs.has_key('updateSetPos'):
			if int(hash['setPos']) == 5:
				hash['setPos'] = -1
			del kargs['updateSetPos']
			del hash['updateSetPos']
		return hash
	
	def week_number_setPos(self,day):
		'''return the week number of the current Month'''
		date = int(day)
		weekN = 0
		if date <= 7:
			return '1'
		else:
			while True:
				if date > 0:
					weekN = weekN + 1
					date = date-7
				else:
					# if weekN == 5: return -1
					return weekN
	
	def expect_str(self, **kargs):
		res = kargs['res']
		if not kargs['expectStr'] in str(res):
			raise Exception('Expect : %s but got: %s'%(kargs['expectStr'], res))
		return 'Got the expected str: ' + kargs['expectStr']
	
	def expect_error(self, **kargs):
		res = kargs['res']
		if not kargs['expectStr'] in str(res):
			raise Exception('Expect error: %s but got: %s'%(kargs['expectStr'], res))
		return 'Got the expected error: ' + kargs['expectStr']
		
	def make_timestr(self, timestamp):
		x = time.localtime(timestamp)
		return time.strftime('%Y%m%dT%H%M%S', x)
		
		