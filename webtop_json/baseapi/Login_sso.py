import requests, os, re, sys, datetime, platform
from Base import Base
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts
from Client import Client

class Login_sso(Base):
	def __init__(self, url):
		Base.__init__(self, url)
		self.url = url
		self.sso_url = self.url.split('dd')[0]
		self.responseData = ''

	def sso_systime(self):
		if 'indows' in platform.system():
			time_delta = 'NOW - 13h'
		else:
			time_delta = 'NOW + 3h'
		return time_delta
		
	def sso_login(self,**kargs):
		print 'login '+kargs['username']
		ssoTokenUrl = self.sso_url + 'sso-token.jsp'
		sso_kargs = {}
		sso_kargs['idex'] = kargs['username']
		now = datetime.datetime.now()
		# sso_kargs['ydtm'] = now.replace(hour=now.hour-12).strftime('%Y%m%d%H%M%S')
		sso_kargs['ydtm'] = ''.join(kargs['time'])
		r = self.client.session.post(ssoTokenUrl,data=sso_kargs)
		sso_token_utility = r.text
		self.client.cookies = r.cookies
		cn2 = re.findall('id="cn2" value="(.*)" ', sso_token_utility)[0]
		
		ssoLogin = self.sso_url + 'sso.jsp'
		r = self.client.session.post(ssoLogin, data={'cn2':cn2})
		self.client.cookies = r.cookies
		self.responseData = r.text
		if 'error code' in r.text:
			raise Exception('response error code: '+r.text.split('<error code="')[1].split('"')[0])   # eg. <error code="QUOTA_EXCEEDED">
		return kargs['username'] + 'signed in!'