import sys, platform, os, json
sys.path.append(os.path.join('..', 'util'))
sys.path.append(os.path.join('..', 'common'))
import SysUtils, re
from AbstractReqBuilder import AbstractReqBuilder

class JSONReqBuilder(AbstractReqBuilder):
	'''
	include all request build method: buildSimpleReq, buildSpecialReq
	include all XML related method
	'''
	def _encodeDictUTF8(self, dict):
		for i in dict:
			if type(dict[i]) == unicode:
				dict[i]=dict[i].encode('utf-8')
		return dict
	
	def _encodeListUTF8(self, list):
		encodedList = []
		for i in list:
			if type(i) == unicode:
				encodedList.append(i.encode('utf-8'))
			else:
				encodedList.append(i)
		return encodedList
	
	def buildSimpleReq(self, request_name, **kargs):
		request_name = SysUtils.getReqByName(request_name)
		# print '~~~~~request_name~~~~~~~'
		# print request_name
		for arg in kargs:
			if '.' in arg:
				request_name = self.setParamsItem(request_name, path = arg, value = kargs[arg])
			else:
				request_name['params'][arg] = str(kargs[arg])
				# request_name['request'][arg] = str(kargs[arg])
		request_name = str(request_name).replace('None', 'null')#for MSG_HEADER_LST
		print request_name
		return request_name
		
	def buildSimpleJson(self, name, value):
		return {name:value}
	
	def setParamsItem(self, request_name, path, value):
		''' for receive different kinds of value and add it to Json, for instance:
				in oringinal request_name -> 'params':{'object':{"type" : "Webtop"}}
				test step -> params.object.name=${address name}
				turn out request -> {'params': {'object': {'type': 'Webtop', 'name': 1420600769}}, '''
		pathStr = ''
		pathL = path.split('.')
		for item in pathL:
			pathStr = pathStr+'["%s"]'%item
		if '{' == str(value)[0]:
			print 'value type: '+str(type(value))
			# print "~~~~~~~~~~222222~~~~~~~~~~"
			# k=value.keys()[0]
			# v=value.values()[0]
			# print request_name
			# print '%s%s[%s]=%s'%('''request_name''', str(pathStr), k,v)
			
			# exec '%s%s[%s]="%s"'%('''request_name''', str(pathStr), k,)
			exec '%s%s=%s'%('''request_name''', str(pathStr), value)
			
		elif '[' == str(value)[0]:
			print 'value is array: '+str(value)
			# value = self._encodeListUTF8(value)
			value = json.dumps(value)
			exec '%s%s=%s'%("request_name", pathStr, value)
		else:
			print 'value is string: '+str(value)
			if '"' in str(value):
				value = value.replace('"','&quot;')
			exec '%s%s="%s"'%("request_name", pathStr, value)
		return request_name
			
	def addDictItem(self):
		pass
	
	
	
		
		


		
		
		
		
if __name__=='__main__':
	reqbuilder = XMLRequestBuilder()
	test = reqbuilder.buildSimpleReq('msgsendRequest', True, body=4, to='888')
	print test