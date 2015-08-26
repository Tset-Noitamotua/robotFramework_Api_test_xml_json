import sys, datetime, re, os, platform, copy
sys.path.append(os.path.join('..', 'reqbuilder'))
sys.path.append(os.path.join('..', 'const'))
sys.path.append(os.path.join('..', 'exception'))

import JSONReqConsts, DefaultReqParams
from JSONReqBuilder import JSONReqBuilder
#from XMLResChecker import XMLResChecker
from TestCodeException import TestCodeException
REQ_FORMAT = 'json'

	

#todo :create object according to json/xml

def getRequestBuilder():
	return eval('%s'%(REQ_FORMAT.upper() + 'ReqBuilder()'))
'''
def getResChecker():
	return eval('%s'%(REQ_FORMAT.upper() + 'ResChecker()'))
'''	
def getReqByName(req_name):
	request_dict = eval('%s'%(REQ_FORMAT.upper() + 'ReqConsts.' + req_name))
	return copy.deepcopy(request_dict) 

def getDefaultParams(req_name):
	return eval('%s'%('DefaultReqParams.' + req_name))
	
def getUtilName():
	return eval(REQ_FORMAT.upper() + 'Utils')

#other funcs
def getFirstItem(exp_str, source_str):
	target_list = re.findall(exp_str, source_str)
	if len(target_list) > 0:
		result = target_list[0]
		return result
	else:
		raise TestCodeException('Can\'t find %s in response!'%exp_str)
	
def findAll(exp_str, source_str, s_mode=False):
	return re.findall(exp_str, source_str)
	
def getTimeDelta(ymd=''):
	'''ymd='2014-06-30' '''
	ct = ymd.split('-')
	time1970n = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
	currentT = datetime.datetime.strptime('%s-%s-%s'%(ct[0],ct[1],ct[2]), '%Y-%m-%d')
	deltaTime = currentT - time1970n
	return deltaTime.days*24*60*60*1000

def getStartTime(timeUnit='days', plus='10'):
	currentTime = datetime.datetime.now()
	plus = int(plus)
	exec 'startD = currentTime - datetime.timedelta(%s = plus)'%timeUnit
	exec 'endD = currentTime + datetime.timedelta(%s = plus)'%timeUnit
	startTime = str(getTimeDelta(ymd=str(startD).split(' ')[0]))
	return startTime

def getEndTime(timeUnit='days', plus='10'):
	currentTime = datetime.datetime.now()
	plus = int(plus)
	exec 'startD = currentTime - datetime.timedelta(%s = plus)'%timeUnit
	exec 'endD = currentTime + datetime.timedelta(%s = plus)'%timeUnit
	endTime = str(getTimeDelta(ymd=str(endD).split(' ')[0]))
	return endTime
	
def getDateDelta(timeUnit='days', plus='10'):
	self.now = datetime.datetime.now()
	plus = int(plus)
	exec 'startD = self.now - datetime.timedelta(%s = plus)'%timeUnit
	exec 'endD = self.now + datetime.timedelta(%s = plus)'%timeUnit
	self.startTime = str(getTimeDelta(ymd=str(startD).split(' ')[0]))
	self.endTime = str(getTimeDelta(ymd=str(endD).split(' ')[0]))
	