import xml.etree.ElementTree as ET
import requests
import WebtopResponseWrap
import datetime, re, os, time, pytz,sys, json
from pytz import timezone
from datetime import datetime, timedelta, tzinfo
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder, TestCodeException, msgconsts
from Prefs import Prefs
import SysUtils

class PrefsLib(Prefs):
	''' Attributes:
	kargs key from config resource must be exactly same as request attribute name
	rtkey as attribute from config resource will return request string istead of return response string
	'''
	def __init__(self,url):
		Prefs.__init__(self, url)
		self.url = url

	def set_calendar_prefs(self,**kargs):	
		'''
		input:
			name: a setting name
		
		description:
			iterator all value of each settings
		'''
		pref_key_name = kargs['name']
		value_list = SysUtils.getDefaultParams('CAL_PREFS_DEFAULT_VALUE')[pref_key_name]
		for value in value_list:
			time.sleep(1)
			param_dict = {pref_key_name : value }
			res = self.set_mail_prefs(**param_dict)

	def check_mail_prefs(self, **kargs):
		expect = bool(kargs['expect'])
		kargs.pop('expect')
		res = self.get_prefs()
		print res
		bAllSet = True
		try:
			res_dict = json.loads(res)
		except Exception, e:
			print 'json loads excep'
			raise e
		for key,value in kargs.items():
			print '############################3'
			print res_dict.has_key(key)
			print res_dict[key]
			if res_dict.has_key(key) and res_dict[key] == value:
				pass
			else:
				bAllSet = False
		
		print bAllSet
		print expect
		if bAllSet^expect:
			raise Exception('Failed to set all prefs')
		else:
			return 'Sueccesfully set prefs %s'%str(kargs)
				
# ------------- user ------------
	def get_current_user_info(self):
		try:
			response = self.request_send('GET_CURRENT_USER_INFO')
			return response
		except Exception, e:
			raise Exception('GET_CURRENT_USER_INFO failed - %s'%str(e))	
			
	def check_user_info_fields_res(self, **kargs):
		# exp_list = kargs['field_list']
		if type(kargs['res']) in [str, unicode] : hash = eval(kargs['res'])
		else:  hash = kargs['res']
		failedL = []
		for exp_field in kargs['field_list']:
			if not hash.has_key(exp_field):
				failedL.append(exp_field)
		if failedL:
			print 'expect--- ' + str(failedL)
			raise Exception('Not found '+str(exp_field))
		return 'All checked'
			
			
			

				
#-----time zone test for other services-----	
	def get_field_value(self, response, fieldName):
		#find values from response: esp -> received-date="1407219008000" 
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

	
	
	
	