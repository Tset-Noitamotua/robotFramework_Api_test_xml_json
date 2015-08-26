import requests, os, re, sys, platform, json
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils
from APIException import APIException
import SysUtils

class Client:
	session = requests.session() # unique session for all apps, use CommonLib.session, DONOT use self.session!
	cookies = None
	large_file_upload_cookies = None

	def __init__(self,url):
		self.url = url

	def send(self, request='', url='', method=''):
		if method == 'post2r':
			r = Client.session.post(url, data={'r':request}) # CommonLib.session.post
			jsonRes = False
		else:
			r = Client.session.post(self.url, data=request)
			jsonRes = True
			
		#Client.cookies = r.cookies #for upload
		if 'auth.login' in request:
			Client.cookies = r.cookies #for upload
		if 'auth.logout' in request:	
			Client.cookies = None

		#for user logout
		if r.text == '(^_^)/\n':
			return r.text
		
		#save large file cookies
		if 'fileUpload.prepareUpload' in request:
			Client.large_file_upload_cookies = r.cookies #for large file upload

		if jsonRes:
			resJn = json.loads(r.text,encoding="utf-8")
			if 'error' in r.text:
				raise APIException(str(resJn['error']).encode('utf-8'))
			if resJn.has_key('result'):
				resultStr = str(resJn['result'])
				# return json.dumps(eval(resultStr))
				return json.dumps(eval(resultStr)).replace(' null','\"\"').replace(' true','\"True\"').replace(' false','\"False\"')
			else:
				# return json.dumps(eval(r.text))
				return json.dumps(eval(r.text)).replace(' null','\"\"').replace(' true','\"True\"').replace(' false','\"False\"')
		else:
			if 'error' in r.text:
				raise APIException(r.text)
			else: return r.text

				
		# ------------------------------------------------
		# for i in resJn:
			# if type(resJn[i]) == unicode:
				# resJn[i]=resJn[i].encode('utf-8')
		
		# if 'error' in str(resJn):
			# raise APIException(str(resJn['error']))   # eg. <error code="QUOTA_EXCEEDED">
		# if resJn.has_key('result'):
			# print 'aaaaaaaaaaaaaaaaa'
			# print resJn['result']
			# return resJn['result']
		# else:
			# print 'bbbbbbbbbbbbbbbbb'
			# print resJn
			# return resJn
		