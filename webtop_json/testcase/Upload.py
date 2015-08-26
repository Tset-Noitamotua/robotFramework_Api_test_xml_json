#filename:uploadFile3.py
#module:MultipartPostHandler
import MultipartPostHandler, urllib2, cookielib, time, requests
import json
import sys, os
sys.path.append(os.path.join('..', 'reqbuilder'))
sys.path.append(os.path.join('..', 'baseapi'))
from Client import Client

#return example {"id":"touchx1x1401934333089","filename":"robot-trans_normal.png","contentType":"image\/png","size":7190}
def uploadResource(uploadURL, filePath, fileid = "", fileName = "fileName"):
	if not uploadURL or not filePath:
		raise Exception("UploadResource invalid parameters.")
	if not Client.cookies:
		raise Exception("Client.cookies is None.")
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Client.cookies), MultipartPostHandler.MultipartPostHandler)
	filePath = filePath.encode("gbk")  # chese
	params = {fileid:open(filePath,"rb")}
	print params
	# statinfo = os.stat(filePath)
	# file_size = statinfo.st_size
	# filecreated = str(int(statinfo.st_ctime)) + '000'
	# filemodified = str(int(statinfo.st_mtime)) + '000'
	# fitletype = os.path.splitext(fileName)[-1][1:]
	
	urlStr = uploadURL + '&fileid=' + fileid 
	# urlStr = uploadURL + '&fileid=' + fileid + '&filename=' + fileName + '&totalbytes=' + str(file_size) + '&filetype=' + fitletype + '&filecreated=' + str(filecreated) + '&filemodified=' + str(filemodified)
	urlStr = urlStr.encode("utf-8")
	res = opener.open(urlStr,params)
	time.sleep(5)
	obj = json.loads(res.read())
	if obj["success"] == True:
		return obj["response"]["files"][0]
	else:
		raise Exception("Upload file failed, filePath: " + filePath)
		
# ----------------------
def uploadBigResource(uploadURL, filePath, name="", fileId = "", crc=""):
	if not uploadURL or not filePath:
		raise Exception("UploadResource invalid parameters.")
	if not Client.cookies:
		raise Exception("Client.cookies is None.")
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Client.cookies), MultipartPostHandler.MultipartPostHandler)
	filePath = filePath.encode("gbk")  # chese
	body_param = {name:open(filePath,"rb")}
	url_params = '{"fileId":"%s","crc":"%s"}'%(fileId,crc)
	
	urlStr = uploadURL + str(url_params).encode("utf-8")
	# urlStr = urlStr.encode("utf-8")
	res = opener.open(urlStr,body_param)
	time.sleep(5)
	obj = json.loads(res.read())
	if obj["success"] == True:
		return obj["response"]["files"][0]
	else:
		raise Exception("Upload file failed, filePath: " + filePath)
		
		
def getResource(url):
	if not Client.cookies:
			raise Exception("Client.cookies is None.")
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Client.cookies))
	# request = urllib2.Request(url.encode("ascii"))
	# request.add_header('Kept Alive', 'No')
	# response = urllib2.urlopen(request)

	sock = opener.open(url.encode("ascii"))
	time.sleep(5)
	return sock
	
def Get_File_Crc(url):

	f = open(url, "r")  
	crc = binascii.crc32(f.read())  
	f.close()  
		
		
			
			