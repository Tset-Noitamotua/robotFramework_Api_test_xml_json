import xml.etree.ElementTree as ET
import requests
import RequestLib, CommonLib, WebtopResponseWrap
import datetime, re, os, time, pytz
from pytz import timezone
from datetime import datetime, timedelta, tzinfo

class PrefsLib():
	''' Attributes:
		kargs key from config resource must be exactly same as request attribute name
	    rtkey as attribute from config resource will return request string istead of return response string
	'''
	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)
		
	def set_profile(self, **kargs):
		'''Attributes:
			kargs['fistName']
			kargs['lastName']
			kargs['mailAddress']
			kargs['userMoblie']	'''
			
		request = RequestLib.profileSettings%(kargs['fistName'],kargs['lastName'],kargs['mailAddress'],kargs['userMoblie'],kargs['fistName']+' '+kargs['lastName'])
		response = self.common.request_send(request)
		expect = 'mailpreference id="%s" realName="%s"'%(kargs['mailAddress'],kargs['fistName']+' '+kargs['lastName'] )
		
		if expect in response:
			return 'Set succesfully: ' + response.split('<mailPreference action="save">')[1]
		else:
			raise Exception('Profile failed to be setted')
		
	def return_zones_byGmt(self, response, namesL):
		GMTs = re.findall('.*<zone id=".*" name="\[GMT (.*)\] .*" offset=".*/>.*', response.replace('><','>\n<'))
		newGmts=[GMTs[0]]
		index=[0]
		newNames = []
		for n in range(1,len(GMTs)):
			if GMTs[n] not in newGmts:
				newGmts.append(GMTs[n])
				index.append(n)
				
		for i in index:
			newNames.append(namesL[i])
		print 'test %d each GMT zones %s'%(len(newNames),str(newNames))
		return newNames
		
	def list_timezones(self):
		tzResp = self.common.request_send(RequestLib.timezonelist)
		self.tzHash = {}
		self.tzNames = re.findall('.*<zone id="(.*)" name=.* offset=.*', tzResp.replace('><','>\n<'))
		if len(self.tzNames) > 39:
			print 'Get %s timezones from timezone list request'%len(self.tzNames)
			self.tzNames = self.return_zones_byGmt(response=tzResp, namesL=self.tzNames)
		return self.tzNames
	
	def set_timezones(self, specific=False):
		'''
			Set Asia/Hong_Kong(GMT+8:00) to use in other step
			Set setHK=False to get all timezones/GMT by timezonelist request for the current build 
			'''
		if specific:
			resp = self.common.request_send(RequestLib.timezoneSet%specific)
			if 'ok' in resp:
				return specific+' is set!'
			else:
				raise Exception('Failed to set '+specific)
		else:
			self.list_timezones()
			passLog = ''	
			failedLog = ''	
			for tz in self.tzNames:
				self.common.request_send(RequestLib.timezoneSet%tz)
				time.sleep(1)
				currentTZResp = self.common.request_send(RequestLib.timezoneGet)
				if '<timezone action="get"><zone id="%s"'%tz in currentTZResp:
					passLog = passLog + tz + ' ;\n'
					pass
				else:
					failedLog = failedLog + tz + ' not get; \n'
					pass
			if not failedLog:
				return 'timezone(s) can be setted as current timezone'
			else:
				raise Exception('\n-----failedLog:\n'+failedLog+'\n---------------------\n-----passLog:\n'+passLog)
				
	def set_languages(self):
		languageList = ['zh_CN', 'zh_TW', 'ja_JP', 'it_IT', 'fr_FR', 'de_DE', 'en_US']
		passLog = ''
		failedLog = ''
		for language in languageList:
			self.common.request_send(RequestLib.singlePrefSet%('LocaleLanguage',language))
			expect = 'pref name="attr.user.LocaleLanguage">%s</pref>'%language
			response = self.common.request_send(RequestLib.prefsGet)
			if expect in response:
				passLog = passLog + language +';'
			else:
				failedLog = failedLog + language +';'
				
		if failedLog:
			raise Exception('\n-----failedLog:\n'+failedLog+'\n---------------------\n-----passLog:\n'+passLog)
		else:
			return 'All Seven languages can be setted as current language - ' + str(languageList)
				
	def set_dateformats(self):
		dateformatList = ['DD/MM/YYYY', 'DD/MM/YY', 'MM/DD/YYYY', 'YYYY/MM/DD']
		passLog = ''
		failedLog = ''
		for dateformat in dateformatList:
			self.common.request_send(RequestLib.singlePrefSet%('DateFormat',dateformat))
			expect = '<pref name="attr.user.DateFormat">%s</pref>'%dateformat
			response = self.common.request_send(RequestLib.prefsGet)
			if expect in response:
				passLog = passLog + dateformat +';'
			else:
				failedLog = failedLog + dateformat +';'
				
		if failedLog:
			raise Exception('\n-----failedLog:\n'+failedLog+'\n---------------------\n-----passLog:\n'+passLog)
		else:
			return 'All Four dateformat can be setted as current settings - ' + str(dateformatList)
	
	def set_timeformats(self):
		timeformat24h = ['TRUE','FALSE']
		passLog = ''
		failedLog = ''
		for timeformat in timeformat24h:
			self.common.request_send(RequestLib.singlePrefSet%('24HourTimeFormatFlag',timeformat))
			expect = '<pref name="attr.user.24HourTimeFormatFlag">%s</pref>'%timeformat
			response = self.common.request_send(RequestLib.prefsGet)
			if expect in response:
				passLog = passLog + timeformat +';'
			else:
				failedLog = failedLog + timeformat +';'
		if failedLog:
			raise Exception('\n-----failedLog:\n'+failedLog+'\n---------------------\n-----passLog:\n'+passLog)
		else:
			return 'Both Two modes of timeformat(24h) can be setted as current settings - ' + str(timeformat24h)
	

#-----time zone test for other services-----	
	def get_field_value(self, response, fieldName):
		'''find values from response: esp -> received-date="1407219008000" '''
		fieldValue = re.findall(' %s="([0-9T]+)"'%fieldName, response)[0]
		return fieldValue
	
	def return_locals_expect(self, hkTimeStamp= 1407294944000, checkFormat= '%Y%m%dT%H%M%S',timezones=['Europe/London']): # return one local time base on timezone attr
		timeTuple = time.localtime(float(hkTimeStamp/1000))
		hk=timezone('Asia/Hong_Kong')
		hk_dt=hk.localize(datetime(timeTuple.tm_year, timeTuple.tm_mon, timeTuple.tm_mday, timeTuple.tm_hour, timeTuple.tm_min, timeTuple.tm_sec))
		print 'hk time is '+str(hk_dt)
		
		zones = []
		for tz in self.tzNames:
			zoneExp = {}
			zone = pytz.timezone(tz)
			zone_dt = hk_dt.astimezone(zone)
			expectTime = zone_dt.strftime(checkFormat)

			zoneExp['name'] = tz
			zoneExp['expTime'] = expectTime	
			zones.append(zoneExp)
		print str(len(zones)) +'timezones expectation ready '
		return zones
			
	
	
	
	
	