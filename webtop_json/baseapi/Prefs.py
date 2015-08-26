import sys, os
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Base import Base

class Prefs(Base):
	def __init__(self, url):
		Base.__init__(self, url)
		
		
	def bootstrap_getConfig(self):
		try:
			response = self.request_send('BOOTSTRAP_GET_CONFIG')
			return response
		except Exception, e:
			raise Exception('BOOTSTRAP_GET_CONFIG failed - %s'%str(e))
		
	def set_prefs(self, **kargs):
		try:
			response = self.request_send('PREFS_SET', **kargs)
			return response
		except Exception, e:
			raise Exception('PREFS_SET failed - %s'%str(e))

	def set_prefs_id(self, **kargs):
		try:
			url = kargs['url']
			del kargs['url']
			request = self.request_send('PREFS_SET_GENERAL_PREFS', return_req=True, **kargs)
			req_list = [eval(request)]
			response = self.post_to_r(str(req_list), url)
			return response
		except Exception, e:
			raise Exception('PREFS_SET_GENERAL_PREFS failed - %s'%str(e))
		
	def set_mail_prefs_id(self, **kargs):
		try:
			url = kargs['url']
			del kargs['url']
			request = self.request_send('MAIL_PREFERENCE_SAVE', return_req=True, **kargs)
			req_list = [eval(request)]
			response = self.post_to_r(str(req_list), url)
			return response
		except Exception, e:
			raise Exception('MAIL_PREFERENCE_SAVE failed - %s'%str(e))

		
			
	def get_prefs(self, **kargs):
		try:
			response = self.request_send('PREFS_GET', **kargs)
			return response
		except Exception, e:
			raise Exception('PREFS_GET failed - %s'%str(e))
			
	def resource_download(self, **kargs):
		try:
			response = self.request_send('RESOURCE_DOWNLOAD', **kargs)
		except Exception, e:
			raise Exception('RESOURCE_DOWNLOAD failed - %s'%str(e))
			
	def resource_upload(self, **kargs):
		try:
			response = self.request_send('RESOURCE_UPLOAD', **kargs)
		except Exception, e:
			raise Exception('RESOURCE_UPLOAD failed - %s'%str(e))
			
			
			
			
	#?	----------
	def set_mail_prefs(self,**kargs):
		'''
		kargs['setDefault'] -> pre-steps: set default prefs 
		'''
		try:
			response = self.request_send('PREFS_SET_TEMPLATE', **kargs)
		except Exception, e:
			raise Exception('Failed to set prefs - %s'%str(e))	

	def set_mail_preference(self, **kargs):
		try:
			response = self.request_send('MAIL_PREFERENCE_SAVE', **kargs)
		except Exception, e:
			raise Exception('Failed to set mail preference - %s'%str(e))

	def set_empty_folder_logout(self, **kargs):
		try:
			response = self.request_send('PREFS_EMPTY_TRASH_WHEN_LOGOUT', **kargs)
			return response
		except Exception, e:
			raise Exception('Set empty trash when logout failed - %s'%str(e))
			
	def load_mail_preference(self,**kargs):
		try:
			response = self.request_send('MAIL_PREFERENCE_LOAD', **kargs)
			return response
		except Exception, e:
			raise Exception('Load mail preferences failed - %s'%str(e))
	
	
	# This was removed from webtop api
	# def set_mobile_mail_preference(self,**kargs):
		# try:
			# response = self.request_send('MOBILE_MAIL_PREFERENCE_SAVE', **kargs)
		# except Exception, e:
			# raise Exception('Failed to set mail preference - %s'%str(e))	

	def load_mobile_mail_preference(self,**kargs):
		try:
			response = self.request_send('MOBILE_MAIL_PREFERENCE_LOAD', **kargs)
			return response
		except Exception, e:
			raise Exception('Load mail preferences failed - %s'%str(e))