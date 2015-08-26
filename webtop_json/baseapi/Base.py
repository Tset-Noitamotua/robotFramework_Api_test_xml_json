import logging
import logging.config
import sys, platform, os
sys.path.append(os.path.join('..', 'util'))
sys.path.append(os.path.join('..', 'logging.conf'))
from ImpLibs import consts, reqbuilder
import SysUtils, Client

class Base(object):
	'''
	include all mail APIs
	'''

	def __init__(self, url):
		self.client = Client.Client(url)
		self.reqBuilder = SysUtils.getRequestBuilder()

	def request_send(self, req_name='',return_req=False, **kargs): # either:return request, or:send request as normal json request
		try:
			request = self.reqBuilder.buildSimpleReq(request_name=req_name, **kargs)
			if return_req: 
				return str(request)
			else:
				response = self.post_request(request)
				return str(response)
		except Exception, e:
			raise e
	
	def post_request(self,request): # first way to send request: normal json request
		response = self.client.send(request)
		return str(response)
	
	
	def post_to_r(self, request, url): # second way to send request: post origin request(will include in r) to url
		try:
			response = self.client.send(request, url, method='post2r')
			return str(response)
		except Exception, e:
			raise e
	
		
	
#if __name__=='__main__':
	#mailobj = APIPub('http://rwc-hinoki06.owmessaging.com:8080/kiwi-octane-rel/dd')
	#test = mailobj.send_request(XMLRequestConsts.MSG_SEND, body=4, to='888')
	#print test