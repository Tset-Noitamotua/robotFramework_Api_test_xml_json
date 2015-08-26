import sys, platform, os
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Base import Base
import SysUtils

class FileUpload(Base):
	'''
	include all file upload APIs
	'''
	def __init__(self, url):
		Base.__init__(self, url)

	def get_config(self, **kargs):
		try:
			response = self.request_send('UPLOAD_GETCONFIG', **kargs)
			return response
		except Exception, e:
			raise Exception('Get upload config failed - %s'%str(e))
			
	def prepare_upload(self, **kargs):
		try:
			response = self.request_send('UPLOAD_PREPARE', **kargs)
			return response
		except Exception, e:
			raise Exception('Prepare upload failed - %s'%str(e))
			
	def file_upload(self, **kargs):
		try:
			response = self.request_send('UPLOAD_UPLOAD', **kargs)
			return response
		except Exception, e:
			raise Exception('Upload file failed - %s'%str(e))
			
	def clear_file(self, **kargs):
		try:
			response = self.request_send('UPLOAD_CLEARFILE', **kargs)
			return response
		except Exception, e:
			raise Exception('Clear file failed - %s'%str(e))
			
	def clear_all(self, **kargs):
		try:
			response = self.request_send('UPLOAD_CLEARALL', **kargs)
			return response
		except Exception, e:
			raise Exception('Clear ALL failed - %s'%str(e))
			
	def get_progress(self, **kargs):
		try:
			response = self.request_send('UPLOAD_GET_PROGRESS', **kargs)
			return response
		except Exception, e:
			raise Exception('Get Progress failed - %s'%str(e))
			
	def pause_upload(self, **kargs):
		try:
			response = self.request_send('UPLOAD_PAUSE', **kargs)
			return response
		except Exception, e:
			raise Exception('Pause file failed - %s'%str(e))
		
	def resume_upload(self, **kargs):
		try:
			response = self.request_send('UPLOAD_RESUME', **kargs)
			return response
		except Exception, e:
			raise Exception('Resume file failed - %s'%str(e))

	def set_rate(self, **kargs):
		try:
			response = self.request_send('UPLOAD_SET_RATE', **kargs)
			return response
		except Exception, e:
			raise Exception('Set rate failed - %s'%str(e))	

	def crc_verify(self, **kargs):
		try:
			response = self.request_send('UPLOAD_VERIFY_CRC', **kargs)
			return response
		except Exception, e:
			raise Exception('Crc verify failed - %s'%str(e))
			