#filename:uploadFile3.py
#module:MultipartPostHandler
import MultipartPostHandler, urllib2, cookielib, time, requests
import json
import CommonLib

#return example {"id":"touchx1x1401934333089","filename":"robot-trans_normal.png","contentType":"image\/png","size":7190}
def uploadResource(uploadURL, filePath, fileid = "", fileName = "fileName"):
		if not uploadURL or not filePath:
			raise Exception("UploadResource invalid parameters.")
		if not CommonLib.CommonLib.cookies:
			raise Exception("CommonLib.cookies is None.")
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CommonLib.CommonLib.cookies), MultipartPostHandler.MultipartPostHandler)
		filePath = filePath.encode("gbk")  # chese
		params = {fileName:open(filePath,"rb")}
		tokenValue = CommonLib.CommonLib.cookies["webtoptoken"]
		sessionId = CommonLib.CommonLib.cookies["webtopsessionid"]
		urlStr = uploadURL % (tokenValue, sessionId)
		if fileid != "":
			urlStr = urlStr + "&fileid=" + fileid
		urlStr = urlStr.encode("utf-8")
		res = opener.open(urlStr,params)
		time.sleep(5)
		obj = json.loads(res.read())
		if obj["success"] == True:
			return obj["response"]["files"][0]
		else:
			raise Exception("Upload file failed, filePath: " + filePath)
		
def getResource(url):
	if not CommonLib.CommonLib.cookies:
			raise Exception("CommonLib.cookies is None.")
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CommonLib.CommonLib.cookies))
	# request = urllib2.Request(url.encode("ascii"))
	# request.add_header('Kept Alive', 'No')
	# response = urllib2.urlopen(request)

	sock = opener.open(url.encode("ascii"))
	time.sleep(5)
	return sock
		
		
		
			
			