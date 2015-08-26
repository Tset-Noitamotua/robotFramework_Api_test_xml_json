import datetime, re, os, sys, time, datetime, copy, requests, cgi, platform, json, binascii, urllib2, MultipartPostHandler
import xml.etree.ElementTree as ET
import WebtopResponseWrap, Upload, SysUtils #PrefsLib,
sys.path.append(os.path.join('..', 'util'))
import cookielib
''' 
if 'indows' in platform.system():
	sys.path.append('..\util')
else:
	sys.path.append('../util')
'''
#from ImpLibs import consts, utils, reqbuilder, msgconsts
from ImpLibs import *
from FileUpload import FileUpload
from Client import Client
from urllib import quote, urlencode, unquote
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import poster

import mimetypes
import mimetools

class FileUploadLib(FileUpload):

	def __init__(self, url):
		FileUpload.__init__(self, url)
		self.url = url

	def Get_File_Crc(self, **kargs):
		filename = kargs['fname']
		if 'indows' in platform.system():
			filePath = os.getcwd() + '\\files\\' + filename
		else:
			filePath = os.getcwd() + '/files/' + filename
		f = None
		try:
			f = open(filePath, "r")  
			crc = binascii.crc32(f.read())  
			
			return hex(crc)[2:]
		except Exception, e:
			raise e
		finally:
			f.close()
			
	def Get_File_Size(self, **kargs):
		filename = kargs['fname']
		if 'indows' in platform.system():
			filePath = os.getcwd() + '\\files\\' + filename
		else:
			filePath = os.getcwd() + '/files/' + filename
		try:
			statinfo = os.stat(filePath)
			file_size = statinfo.st_size
			return file_size
		except Exception, e:
			raise e
	
	def get_fileid_by_prepare_upload(self, **kargs):
		tempId = kargs['tempId']
		kargs.pop('tempId')
		try:
			res = self.prepare_upload(**kargs)
			return json.loads(res)[tempId]
		except Exception, e:
			raise e

	def upload_file(self,**kargs):
		self.fidL = []
		for file in kargs['fname'].split():
			self.uploadURL = kargs['url']
			if 'indows' in platform.system():
				self.filePath = os.getcwd() + '\\files\\' + file
			else:
				self.filePath = os.getcwd() + '/files/' + file
			fileid = datetime.datetime.now().strftime('%y%m%d%S')
			attach = Upload.uploadResource(self.uploadURL, self.filePath, fileid, fileName = kargs['fname'])
			self.fidL.append(attach['id'])
		self.fids = ','.join(self.fidL)
		print '[files]: ' + kargs['fname'] +' | [file id]: '+ self.fids
		print 'Successfully upload attachments!'
		return self.fids
	
	def file_upload_postReq_json(self,**kargs):
		for file in kargs['fname'].split():
			self.uploadURL = kargs['url']
			if 'indows' in platform.system():
				self.filePath = os.getcwd() + '\\files\\' + file
			else:
				self.filePath = os.getcwd() + '/files/' + file
		fileid = datetime.datetime.now().strftime('%d%H%M%S')
		Upload.uploadBigResource(kargs['url']+'?r=fileUpload.upload', self.filePath, name=fileid, fileId=kargs['fileId'], crc=kargs['crc'])
	
	
	def resource_upload_postReq_json(self,**kargs):
		post_url = kargs['url']
		request_name = kargs['req_name']
		del kargs['url'], kargs['req_name']
		ignore = False
		if kargs.has_key('return_response'): 
			ignore=True
			del kargs['return_response']
		resource_upload = self.reqBuilder.buildSimpleReq(request_name, **kargs)
		request = 'resource.upload' + resource_upload
		res = self.post_to_r(request, post_url)
			
	def resource_download_postReq_json(self, **kargs): # for export,download,check inline.. - works for different descriptors for download
		'''	download small file by post Json request. i.e:
			url=${resource_load}    req_name=RESOURCE_DOWNLOAD_EVENTS
			buildSimpleReq for descriptor by other kargs: 
				descriptor.calendarId=${cal ids}    descriptor.filename=robotExportEvent.ics   
			if has kargs['return_response']: just will return the response
		'''
		inline = dataUri = dimensions = False
		post_url = kargs['url']
		request_name = kargs['req_name']
		del kargs['url'], kargs['req_name']
		ignore = False
		if kargs.has_key('return_response'): 
			ignore=True
			del kargs['return_response']
			
		if kargs.has_key('inline'):
			inline = True
			del kargs['inline']
			
		resource_download = self.reqBuilder.buildSimpleReq(request_name, **kargs)
		request = 'resource.download' + resource_download
		if inline:
			request = request.replace("}}", '}, "inline":"True" }')
		
		res = self.post_to_r(request, post_url)
		if ignore:
			return res
		if 'BEGIN:' in res and 'END:' in res: return 'Download successful'
		else: raise Exception('Download failed')

#========================================================================================================
	def encode_multipart_formdata(self, fields, files = {}):
		print '--------------------------in encode_multipart_formdata'

		boundary = mimetools.choose_boundary()
		CRLF = '\r\n'
		data = []
		#for key in files:
		data.append('--' + boundary)
		data.append('Content-Disposition: form-data; name="file"; filename="'+ files['filename'] + '"')
		data.append('Content-Type: "' + files['type'] + '"')
		data.append('')
		data.append(files['filedata'])
		data.append('--' + boundary + '--')
		data.append('')
		body = CRLF.join(data)
		content_type = 'multipart/form-data; boundary=%s' % boundary
		print '--------------------------out encode_multipart_formdata'
		return {'content_type':content_type,'body':body}

	def httpopenfile(self, filename):
		print '--------------------------in httpopenfile'
		filePath = ''
		if 'indows' in platform.system():
			filePath = os.getcwd() + '\\files\\' + filename
		else:
			filePath = os.getcwd() + '/files/' + filename

		f = open(filePath.encode("gbk"),'rb')
		data = f.read()
		f.close()
		statinfo = os.stat(filePath)
		filesize = statinfo.st_size
		
		filename = "blob"
		filetype = "application/octet-stream"
		fileInfo = {'filename':filename,'size':filesize,'type':filetype,'filedata':data}
		print '--------------------------out httpopenfile'
		return fileInfo
		
		
	def sendwb(self, url, file_path, crc, file_id):
		print '--------------------------in sendwb'
		#deal with cookies
		if not Client.large_file_upload_cookies:
			raise Exception("Client.large_file_upload_cookies is None.")
		if not Client.cookies:
			raise Exception("Authentication cookies(Client.cookies) is None.")
		#try to merge cookies. find a better way if you can.
		templist = url.split('/')
		host = templist[2].split(':')[0]
		uri = '/' + templist[3]
		for key in Client.large_file_upload_cookies._cookies[host][uri]: 
			Client.cookies._cookies[host][uri][key] = Client.large_file_upload_cookies._cookies[host][uri][key]
		opener = poster.streaminghttp.register_openers()
		opener.add_handler(urllib2.HTTPCookieProcessor(Client.cookies))	
		#post url
		file_path = file_path.encode("gbk")  # chese
		url_param = 'fileUpload.upload{%22fileId%22:%22' + file_id.encode('utf-8') + '%22,%20%22crc%22:%22' + crc + '%22}'
		urlStr = url + 'r=' + url_param	
		file = self.httpopenfile(file_path)
		params = self.encode_multipart_formdata({}, files=file)

		req = urllib2.Request(urlStr, data = params['body'])
		req.add_header('Content-Type', params['content_type'])
		req.add_header('Accept-Encoding', 'gzip, deflate')
		req.add_header('Accept', '*/*')		

		resp = urllib2.urlopen(req)
		print '--------------------------out sendwb'
		return resp;
		
	def upload_file_test(self, **kargs):
		crc = kargs['crc']
		file_id = kargs['fileId']
		file_upload_path = kargs['uploadPath']
		file_path = kargs['fname']	
		resp = self.sendwb(file_upload_path, file_path, crc, file_id)
		
		time.sleep(5)
		obj = json.loads(resp.read())
		if 'error' in str(obj):
			raise Exception("Upload file failed, filePath: " + file_upload_path)
