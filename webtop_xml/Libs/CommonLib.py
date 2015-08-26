import requests, os, re, datetime
import RequestLib
import WebtopResponseWrap
import xml.etree.ElementTree as ET

class CommonLib:
	session = requests.session() # unique session for all apps, use CommonLib.session, DONOT use self.session!
	cookies = None
	def __init__(self,url):
		self.url = url
		self.sso_url = self.url.split('dd')[0]
		self.responseData = ''
		
	def user_login(self,**kargs):
		CommonLib.useraddress = kargs['username']
		return self.request_send(RequestLib.loginRequest,kargs)
		
	def sso_login(self,**kargs):
		ssoTokenUrl = self.sso_url + 'sso-token.jsp'
		sso_kargs = {}
		sso_kargs['idex'] = kargs['username']
		now = datetime.datetime.now()
		sso_kargs['ydtm'] = now.replace(hour=now.hour-12).strftime('%Y%m%d%H%M%S')
		sso_token_utility = CommonLib.session.post(ssoTokenUrl,data=sso_kargs).text
		cn2 = re.findall('id="cn2" value="(.*)" ', sso_token_utility)[0]
		
		ssoLogin = self.sso_url + 'sso.jsp'
		r = CommonLib.session.post(ssoLogin, data={'cn2':cn2})
		CommonLib.cookies = r.cookies
		self.responseData = r.text
		if 'error code' in r.text:
			raise Exception('response error code: '+r.text.split('<error code="')[1].split('"')[0])   # eg. <error code="QUOTA_EXCEEDED">
		return kargs['username'] + 'signed in!'
		
		
	def user_logout(self):
		return self.request_send(RequestLib.logoutRequest)
		
	def request_send(self,request,hash={},getRes=False):
		# send request and check request data format
		for key,value in hash.items():
			if ' '+key+'=' in request:
				request = request.replace(' '+key+'="%s',' '+key+'="'+value)
			if '<' + key + '>%s</' + key + '>' in request:
				request = request.replace('<' + key + '>%s</' + key + '>','<' + key + '>' + value + '</' + key + '>')
				
		requestData = request.replace('%s','')
		if getRes:
			return requestData
		r = CommonLib.session.post(self.url,data={'r':requestData}) # CommonLib.session.post
		# for attr in CommonLib.session.__dict__:
			# print attr
		#if not CommonLib.cookies:
		#	CommonLib.cookies = r.cookies
		CommonLib.cookies = r.cookies
		self.responseData = r.text
		if 'error code' in r.text:
			raise Exception('response error code: '+r.text.split('<error code="')[1].split('"')[0])   # eg. <error code="QUOTA_EXCEEDED">

		if 'rtkey' in hash:
			return request
			
		return self.responseData

		
	def simple_post(self, url, data={}):
		r = CommonLib.session.post(url, data)
		print r
		
	def check_response(self,needBlocked=False, expectHash={},checkByTimeFlag=False,getID=False):
		# Three ways to check response of the last request
		resultInfo = ''
		id = ''
		
		if checkByTimeFlag:
			if needBlocked:
				if checkByTimeFlag not in self.responseData:
					return 'Message blocked or not find really'
				else:
					raise Exception('Should have blocked but still found: '+checkByTimeFlag)
			else:
				if checkByTimeFlag not in self.responseData:
					raise Exception('expect (%s) not in response'%checkByTimeFlag)
				else:
					resultInfo = 'Checked keywords: ' + checkByTimeFlag + ', '
			
		if expectHash:
			for k,v in expectHash.items():
				keywords = k + '="' + v + '"'
				if keywords not in self.responseData:
					raise Exception('expect: %s is not in %s'%(keywords,self.responseData))
				resultInfo = resultInfo + 'checked hash ok, '
				
		if getID:
			if '_s' in getID:
				idList = re.findall('%s="(\w+)"'%getID.split('_s')[0],self.responseData.replace('><','>\n<'))
				return idList
			else:
				idList = re.findall('%s="(\w+)"'%getID,self.responseData.replace('><','>\n<'))
				if len(idList) == 0:
					raise Exception('No messages found in responseData.')
				return idList[0]
		return resultInfo
		
	def responsePraser(self):
		return self.responseData
		
		
	
	
		
