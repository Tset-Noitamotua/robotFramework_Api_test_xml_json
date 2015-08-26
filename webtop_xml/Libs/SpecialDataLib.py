import datetime, re, os, time, datetime
import CommonLib, MailLib, CalendarLib, PrefsLib, ContactLib, RequestLib

class SpecialDataLib():
	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)

	def getDataList(self,name):
		dataFile = os.getcwd() + '\\special_data.txt'
		dataSource = open(dataFile,'r')
		for line in dataSource.readlines():
			if name in line:
				lineL = line.split()
				if 'space' in line:
					lineL.pop(lineL.index('space'))
					lineL.append(' ')
				lineL.pop(0)
		dataSource.close()
		self.dataList = []
		for char in lineL:
			self.dataList.append(char+ name)
		return self.dataList
		
	def getNewRequest(self,request,name,data):
		if re.findall('%s="(.*)".*'%name,request):
			oldData = re.findall('%s="(.*)".*'%name,request)[0].split('"')[0]	# subject="%s runtime"    <body>automation test content</body>
		if re.findall('<%s>(.*)</%s>'%(name,name),request):
			oldData = re.findall('<%s>(.*)</%s>'%(name,name),request)[0]
		newRequest = request.replace(oldData, data)
		return newRequest
		
	def send_special_data(self, **kargs):
		'''	
			kargs['functionName'] -> send special data by the certain function
			kargs['specialDataName'] -> the attribute or node name(like subject, body) you want to set from request
			kargs['data'] -> the name of bunch of special data from special_data.txt, like mailFolderEscaped 
			kargs['beUpdatedName'] -> (optional) use for the attribute being updated again and again (for test update data with special characters), like 'source' from 'folderrename'
		'''
		functionName = kargs['functionName'] # send_message
		specialDataName = kargs['specialDataName']
		self.getDataList(kargs['data']) # mail_subject -> dataList
		del kargs['functionName']
		
		libsPath = os.getcwd().replace('Testsuite','Libs\\') # get service class name
		for root,folder,files in os.walk(libsPath):
			for file in files:
				if 'Lib.py' in file: # in serviceLib
					sourceFile = open(libsPath+file,'r') # +serviceLib
					libSource = str(sourceFile.readlines()).replace('><','>\n<')
					sourceFile.close()
					if u'def %s(self'%functionName in libSource:
						className = re.findall('.*class (\w+).*' ,libSource)[0]
		
		exec 'service = %s.%s(self.url)'%(className,className) # service class call function to send new requests with data value
		#exec 'originalReq = service.%s(**kargs)'%functionName  # set attributes from outside testcase to Services function
		failedLog = ''
		for dataValue in self.dataList:
			kargs[specialDataName] = dataValue
			try:
				exec 'result = service.%s(**kargs)'%functionName
			except Exception,e:
				failedLog = failedLog + dataValue +': '+  str(e) +'\n' # 
		if failedLog:
			raise Exception('Not all characters passed: \n'+failedLog)
		else:
			return 'All special data passed '+ str(self.dataList)
		
		
		
		
		
		
		
		
	
	
	