import re, os, time, platform, sys
from Crypto.Cipher import AES
import hashlib
sys.path.append(os.path.join('..', 'util'))
from Mail import Mail
from Base import Base
import SysUtils

class SessionTokenLib(Base):
	''' kargs key from config resource must be exactly same as request attribute name
	    rtkey as attribute from config resource will return request string istead of return response string
	'''
	def __init__(self,url):
		Base.__init__(self, url)
		self.url = url
		self.mail = Mail(url)
	
	def __getKey(self):
		key = 'This is insecure, change'
		encryptedKey = hashlib.sha512(key).hexdigest()
		encryptedKey = encryptedKey.decode('hex')
		return encryptedKey[0:16]
	
	def __decrypt(self, encrypedToken): 
		obj = AES.new(self.__getKey(), AES.MODE_ECB)
		decode_hex = encrypedToken.decode('hex')
		crypt = obj.decrypt(decode_hex)
		return crypt

	def __encrypt(self, originToken):
		BS = 16
		pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
		#unpad = lambda s : s[0:-ord(s[-1])]
		obj = AES.new(self.__getKey(), AES.MODE_ECB)
		cryptToken = obj.encrypt(pad(originToken))
		return cryptToken.encode('hex')
		
	def api_call_emptyfolder(self,**kargs):
		try:
			emptyFolderRes = self.mail.empty_folder(**kargs)
			domain = re.findall('http://(.*):', kargs['host'])[0]
			originToken = self.client.session.cookies._cookies[domain]['/']['webtoptoken'].value
			token = self.__decrypt(originToken)
			origin_expired_time = re.findall(',([0-9]+),', token)[0]
			return self.client.session.cookies._cookies[domain]['/']['webtopsessionid'].value + ' | ' + origin_expired_time
		except Exception,e:
			if 'AUTHENTICATION_REQUIRED' in str(e):
				return 'AUTHENTICATION_REQUIRED'
			else:
				raise e
		
	def make_expired_token(self,**kargs):
		domain = re.findall('http://(.*):', kargs['host'])[0]
		#find original token
		originToken = self.client.session.cookies._cookies[domain]['/']['webtoptoken'].value
		token = self.__decrypt(originToken)
		origin_expired_time = re.findall(',([0-9]+),', token)[0]
		expiry = kargs['expiry']
		#mock token time expired
		moke_expired_time = int(origin_expired_time) - int(expiry)*60*60*1000
		#make a new encrypted token
		newtoken, number = re.subn(',[0-9]+,', ',' + str(moke_expired_time) + ',', token)
		self.client.session.cookies._cookies[domain]['/']['webtoptoken'].value = self.__encrypt(newtoken)
		#print self.common.session.cookies._cookies
		
	def make_expired_session(self,**kargs):
		domain = re.findall('http://(.*):', kargs['host'])[0]
		self.client.session.cookies._cookies[domain]['/']['webtopsessionid'].value = 'invalidsession'