import datetime, re, os, time, datetime, copy, platform
import xml.etree.ElementTree as ET
import requests
import RequestLib, CommonLib, WebtopResponseWrap, Upload, PrefsLib
from multiprocessing.dummy import Pool

class MailLib():
	''' kargs key from config resource must be exactly same as request attribute name
	    rtkey as attribute from config resource will return request string istead of return response string
	'''
	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)
		self.prefs = ''
	
	def _findFirstUserFolder(self, fromTrash=False):
		folderList = self.list_folder()
		try:
			if fromTrash:
				trashFolder = re.findall(r'fullname="Trash/(.*)" msgcount=',folderList.replace('><','>\n<'))[0]
				if trashFolder:
					return trashFolder
				else:
					return 'no valid folder'
			else:
				fullnamefolderL = re.findall(r'.*fullname="(.*)" msgcount=.*',folderList)
				for fullNameFolder in fullnamefolderL:
					if fullNameFolder not in ['INBOX', 'Drafts', 'Sent', 'spam', 'Spam', 'Trash','SentMail']:
						return fullNameFolder
						break
					else:
						deleteFolder = 'no valid folder'
						pass
		except Exception,e:
			raise Exception(e)
	
	def listSignatureId(self, listFirst=False):
		listSignatureRes =  self.common.request_send(RequestLib.mailSignatureList)
		listSignatureRes = listSignatureRes.replace('><','>\n<')
		signatureIDs = re.findall('<mailsignature id="(.*)" label',listSignatureRes)
		if listFirst:
			return signatureIDs[0]
		else:
			return signatureIDs
	
	def _getTimeDelta(self, ymd=''):
		'''ymd='2014-06-30' '''
		ct = ymd.split('-')
		time1970n = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
		currentT = datetime.datetime.strptime('%s-%s-%s'%(ct[0],ct[1],ct[2]), '%Y-%m-%d')
		deltaTime = currentT - time1970n
		return deltaTime.days*24*60*60*1000
	
	def _getDateDelta(self, timeUnit='days', plus='10'):
		self.now = datetime.datetime.now()
		plus = int(plus)
		exec 'startD = self.now - datetime.timedelta(%s = plus)'%timeUnit
		exec 'endD = self.now + datetime.timedelta(%s = plus)'%timeUnit
		self.startTime = str(self._getTimeDelta(ymd=str(startD).split(' ')[0]))
		self.endTime = str(self._getTimeDelta(ymd=str(endD).split(' ')[0]))
	
	def list_folder(self,checkfolder='',findParent = False):
		'''
		    findParent - find parent folder of 'checkfolder'.
		    checkfolder - check the folder path, on which layer there don't have, 
		    and use findParent to check -> on which layer there already has.'''
		   
		listfolderRes = self.common.request_send(RequestLib.folderlistRequest)
		if findParent:
			while('fullname="'+checkfolder+'"' not in listfolderRes):
				if '/' in checkfolder:
					newfolder = checkfolder.split('/')[-1]
					checkfolder = checkfolder.replace('/'+checkfolder.split('/')[-1],'')
				else:
					newfolder = checkfolder
					checkfolder = ''
					break
			fullpath = [checkfolder,newfolder]
			return fullpath
		else:
			return listfolderRes
	
	def _setPrefValue(self,request,prefsName,prefsValue):
		node = re.findall('<prefs name="%s">.*</prefs>'%prefsName,request)[0]
		newReq = request.replace(node,'<prefs name="%s">%s</prefs>'%(prefsName,prefsValue))
		return newReq
			
	def _removeExternalAccount(self,externalID):
		ExternalDelResp = self.common.request_send(RequestLib.mailExternalAccountDel%externalID)
		if '<status>ok</status>' in ExternalDelResp:
			return 'Existed account delete OK'
		else:
			raise Exception('Failed to delete existed external account ID')
	
	def upload_file(self,**kargs):
		''' Input: kargs['common_upload_url'],kargs['file_name'] (multi attachments by SPACE)
			Save: fileid
			Output: attachment names and ids'''
		self.fidL = []
		for file in kargs['fname'].split():
			self.uploadURL = kargs['url']
			# if 'Sanity' in os.getcwd():
				# cwd = 'Testsuite\Sanity'
			# else:
				# cwd = 'Testsuite'
			# self.filePath = os.getcwd().replace(cwd,'') + 'Libs\\files\\' + file
			if 'indows' in platform.system():
				self.filePath = os.getcwd() + '\\files\\' + file
			else:
				self.filePath = os.getcwd() + '/files/' + file
			fileid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			attach = Upload.uploadResource(self.uploadURL, self.filePath, fileid, fileName = fileid)
			self.fidL.append(attach['id'])
		self.fids = ','.join(self.fidL)
		print '[files]: ' + kargs['fname'] +'|[file id]: '+ self.fids
		print 'Successfully upload attachments!'
		return self.fids
		
	def send_message(self,**kargs):
		kargs['rtkey']=True
		if not kargs.has_key('bodytype'):
			kargs['bodytype'] = 'plain'		
		request = self.common.request_send(RequestLib.msgsendRequest,kargs,getRes=True)
		if kargs.has_key('specialDataName') and (kargs['specialDataName'] == 'img'): # for specialDataLib calling
			return request
		if kargs.has_key('attachment'):
			attachReq = WebtopResponseWrap.WebtopResponseWrap(request)
			attachReq.setElementValue(xPath='mail', valueText='', attrib={'attach-fileid':self.fids})
			request = attachReq.toXML()
		if kargs.has_key('subject'):
			self.runtimekey = request.split('subject="')[1].split('"')[0]
			self.common.request_send(request)
			return self.runtimekey
		
	def send_with_img(self,**kargs):
		'''	same kargs as send mail 
			kargs['smileFace']=${mail_faceImg}, kargs['faceIcon']=1 ~ 49'''
		kargs['specialDataName'] = 'img'
		kargs['bodytype'] = 'html'
		request = self.common.request_send(RequestLib.msgsendRequest,kargs,getRes=True)
		# if not '#' in kargs['smileFace']:
		img = kargs['smileFace'] + kargs['faceIcon'] + '.gif'
		face_img = '&lt;img src=&quot;%s&quot;&gt;&lt;br&gt;'%img
		sendImgReq = request.replace('automation test content', face_img)
		# else:
			# img = kargs['smileFace']
			# face_img = request.replace('automation test content', kargs['smileFace'])
			# sendImgReq = request.replace('automation test content', face_img)
		resp = self.common.request_send(sendImgReq,kargs)
		if '<mail action="msgsend">' in resp and 'ok' in resp:
			print 'Mail is sent with below image body\n: '
			return img
		else:
			raise Exception('Failed to send mail')
		
	def preview_attachments(self,**kargs):
		'''url=${mail_get_attach_url}	folder=INBOX'''
		self.check_message_fetch(**kargs)
		if 'attachment size' not in self.msgFetchResp:
			raise Exception(self.msgFetchResp.split('<body')[1])
		attachN = len(re.findall('<attachment size="',self.msgFetchResp))
		failedResult = ''
		for partN in range(attachN):
			url = kargs['url']%(kargs['folder'],self.msguid,str(partN+1))
			sock = Upload.getResource(url)
			print 'previewing...'+self.msguid
			if str(sock.code) == '200':
				print 'read>>'+str(sock.read(100))
			else:
				failedResult = failedResult + '%s found %s'%(str(partN+1),str(sock.code)) + '\n'
		if failedResult:
			raise Exception('Resource not get %s found!'%str(self.msguid))
		else:
			return 'All esource succesfully get with HTTP code '+str(sock.code)
			
	def open_message(self,**kargs):
		self.common.request_send(RequestLib.msgheaderlist,kargs)
		msguid = self.common.check_response(getID='msg uid')
		url = kargs['hostport'] + RequestLib.saveMailToComputer
		url = url%('', kargs['folder'], msguid) 
		
		code = Upload.getResource(url).code
		if str(code) == '200':
			return 'GET mail %s .eml'%msguid
		else:
			raise Exception('Failed to GET mail %s .eml'%msguid)
			
	def check_message_header(self,**kargs):
		self.msgheaderlistResp = self.common.request_send(RequestLib.msgheaderlist,kargs)
		self.msguid = self.common.check_response(getID='msg uid')
		
		kargs['uidnext'] = self.msguid
		self.common.request_send(RequestLib.msgheaderlistcheck,kargs)
		return self.common.check_response(checkByTimeFlag = self.runtimekey)
		
	def check_message_fetch(self,**kargs):
		''' folder=INBOX 
			kargs['kw']->check keywork 
			html=full
			note: showImg -> expect the actual image, if not expect show actual image -> DONOT pass kargs['kw'] here
			'''
		if not kargs.has_key('html'):
			kargs['html'] = 'text'
		self.common.request_send(RequestLib.msgheaderlist%kargs['folder'])
		self.msguid = kargs['uid']  = self.common.check_response(getID='uid')
		request = RequestLib.msgfetchRequest
		#  showImg -> to show actual image for trust sender, blockImg -> just show blocked img icons and show buttons
		if kargs.has_key('showImg'):  # (normally can received situation do not need to use)
			request = request.replace('></mail>', ' block-ext-images="0" ></mail>')
		if kargs.has_key('blockImg'):
			kargs['kw'] = '&lt;img src="blocked"/&gt;&lt;br&gt;'
		self.msgFetchResp = self.common.request_send(request,kargs)
		try:
			needBlocked = kargs['needBlocked']
		except:
			needBlocked = ''
			
		if kargs.has_key('kw'):
			return self.common.check_response(needBlocked,checkByTimeFlag=kargs['kw'])
		return self.common.check_response(needBlocked,checkByTimeFlag=self.runtimekey)
		
	def check_vCard(self, **kargs):
		'''url=${mail_get_attach_url}'''
		k = {'folder':'INBOX'}
		self.common.request_send(RequestLib.msgheaderlist,k)
		self.msguid = self.common.check_response(getID='msg uid')
		url = kargs['url']%(k['folder'],self.msguid,'1')
		sock = Upload.getResource(url)
		read = sock.read()
		failedResult = ''
		if str(sock.code) == '200':
			if 'BEGIN:VCARD' in read and 'END:VCARD' in read:
				return read
			else:
				raise Exception('vCard canNOT be found from attachment')
		else:
			raise Exception('Cannot GET attachment')
	
	def move_message(self,**kargs):
		'''move the first mail from attribute 'folder' to the first valid created folder, then check destination folder list
			dstfolder -> the destination folder name
			all -> move all messages'''
		idName='uid'
		if kargs.has_key('all'):
			idName='uid_s'
		
		request = self.common.request_send(RequestLib.msgheaderlist,kargs)
		uid = self.common.check_response(getID='uid')
		kargs['uids'] = uid # str(int(uid)+1)
		kargs['uidnext'] = str(int(uid)+1)   # str(int(kargs['uids'])+1)
		if kargs.has_key('all'):
			idlist = self.common.check_response(getID=idName)
			kargs['uids'] = str(','.join(idlist))
			del kargs['all']
		
		if not kargs['dstfolder']:
			kargs['dstfolder'] = self._findFirstUserFolder()
		response = self.common.request_send(RequestLib.msgmove,kargs)
		
		
		if re.findall('affectedmsgcount="(.*)" />',response):
			return 'From %s to %s - Successfully affect: uid%s '%(kargs['folder'],kargs['dstfolder'],kargs['uids'])
		else:
			raise Exception('From %s to %s- Failed affect: uid%s '%(kargs['folder'],kargs['dstfolder'],kargs['uids']))
		
	def save_message_as_draft(self,**kargs):
		saveDraftReq = RequestLib.msgsendRequest.replace('msgsend','msgsaveasdraft').replace('><body>',' auto="false"><body>')
		#if kargs.has_key('specialDataName'): # for specialDataLib calling
		#	return self.common.request_send(saveDraftReq,kargs,getRes=True)
		#else:
		self.saveMsgResp = self.common.request_send(saveDraftReq,kargs)
		uid = self.common.check_response(getID='uid')
		if '<msgsaveasdraft uid="%s"'%uid in self.saveMsgResp:   # str(int(uid)+1)
			return 'Message uid %s is saved as draft'%uid
		else:
			raise Exception('Failed to save uid %s as draft'%uid)
			
	def print_preview_message(self, **kargs):
		self.common.request_send(RequestLib.msgheaderlist,kargs)
		uid = self.common.check_response(getID='msg uid')
		envurl = self.url.replace('/dd','')
		#valid enum values are [none, embeddedOnly, embeddedAndRemote]
		url = envurl +'/bin?r=mail.message.print{accountId:"",folderPath:"%s",messageUid:%s,images:"none"}'%(kargs['folder'],uid)
		print 'url is '+url
		
		sock = Upload.getResource(url)
		if str(sock.code) == '200':
			return 'print preview read 100>>'+str(sock.read(100))
		else:
			raise Exception('%s found %s'%(str(partN+1),str(sock.code)))
		
	def flag_message(self,**kargs):
		'''kargs attributes: 
			flag -> seen/flagged
			UNREAD -> seen, value=0
			READ -> seen, value=1
		'''
		request = self.common.request_send(RequestLib.msgheaderlist,kargs)
		uid = self.common.check_response(getID='uid')
		kargs['uids'] = uid # str(int(uid)+1)
		kargs['uidnext'] = str(int(kargs['uids'])+1)
		
		flagResp = self.common.request_send(RequestLib.msgflag,kargs)
		if 'affectedmsgcount="1"' in flagResp:
			if kargs['flag']=='seen':
				return 'Message uids %s is flagged to be UNREAD'%kargs['uids']
			else:
				return 'Message uids %s is flagged to be FLAGGED'%kargs['uids']
		else:
			raise Exception('Message uids %s is failed to be flagged'%kargs['uids'])

	def report_message(self,**kargs):
		msgheadersResp = self.common.request_send(RequestLib.msgheaderlist,kargs)
		self.spamID, self.spamSubject = re.findall('.*<msg uid="(.*)" subject="(.*)" seen=.* ',msgheadersResp.replace('><','>\n<'))[0]
		self.spamAddr = msgheadersResp.split(self.spamSubject)[1].split('address="')[1].split('" />')[0]
		kargs['uids'] = self.spamID 
		if kargs.has_key('dstfolder'): # mark message as spam
			response = self.common.request_send(RequestLib.msgreport,kargs)
			ok = 'spam'
				
		else: # mark message not as spam
			request = RequestLib.msgreport.replace('junk','notjunk')
			# request = request.replace(kargs['folder'],'INBOX')
			request = request.replace(re.findall('.*(sortby="\w+").*',request)[0], '')
			request = request.replace(re.findall('.*(sortorder="\w+").*',request)[0], '')
			response = self.common.request_send(request%('INBOX',kargs['folder'], self.spamID))
			ok = 'notspam'

		if 'mail action="msgreport"' in response and 'affectedmsgcount="1"' in response:
			print 'Successfully mark (uids%s) as %s message'%(kargs['uids'],ok)
			print 'report: '+self.spamSubject
			return self.spamSubject
		else:
			raise Exception('Failed to mark (uid%s) as %s message'%(kargs['uids'],ok))

	def check_message_header_subject(self,**kargs):
		'''kargs['folder']'''
		response = self.common.request_send(RequestLib.msgheaderlist,kargs)
		if kargs.has_key('subject'): # get expect subject from case kargs
			expect = 'subject="%s"'%kargs['subject']
			print 'expect subject: '+expect
		else: # get expect subject from spam after report spam request
			expect = 'subject="%s"'%self.spamSubject
			print 'expect spam subject: '+expect
			
		if expect in response:
			return '%s is checked in %s'%(expect, kargs['folder'])
		else:
			raise Exception('%s is NOT in %s'%(expect, kargs['folder']))
		
	def search_message(self,**kargs):
		'''	To be used after send mail. default search by -> defaultAttriH, 
			search by -> kargs['text']
			'''
		defaultAttriH = {'sortby':'date', 'sortorder':'desc', 'pieces':'subject,from,recipients,body', 'folders':'INBOX'}
		setAttr = {}
		for i in kargs:
			if i in defaultAttriH:
				defaultAttriH[i] = kargs[i]
			else:
				setAttr[i] = kargs[i]
		
		request = RequestLib.vmsgheaderlist
		if setAttr: # search condition other than defaultAttriH
			wrapReq = WebtopResponseWrap.WebtopResponseWrap(request)
			if kargs.has_key('timeUnit') or kargs.has_key('delta'): # before and end time for search
				self._getDateDelta(kargs['timeUnit'], kargs['delta'])
				del kargs['timeUnit'], kargs['delta']
				wrapReq.setElementValue(xPath='mail', valueText='', attrib={'before':self.startTime, 'after':self.endTime})
				
			wrapReq.setElementValue(xPath='mail', valueText='', attrib=setAttr)
			request = wrapReq.toXML()
			print defaultAttriH
		self.vmsgheaderlistResp = self.common.request_send(request,defaultAttriH)	

		msgcount = self.vmsgheaderlistResp.split('msgcount="')[1].split('"')[0]
		unreadcount = self.vmsgheaderlistResp.split('unreadcount="')[1].split('"')[0]
		if kargs['text'] in self.vmsgheaderlistResp:# and int(msgcount)|int(unreadcount):
			return 'Successfully searched %s mail with %s'%(str(msgcount),kargs['text'])
		else:
			raise Exception('Failed to searched mail with'+kargs['text'])
		
	def delete_message(self):
		kargs = {}
		request = self.common.request_send(RequestLib.msgheaderlist,{'folder':'Trash'})
		uid = self.common.check_response(getID='uid')
		kargs['uids'] = uid # str(int(uid)+1)
		kargs['uidnext'] = str(int(kargs['uids'])+1)
	
		response = self.common.request_send(RequestLib.msgdelete,kargs)
		if 'mail action="msgdelete"' in response and 'affectedmsgcount="1"' in response:
			return 'Successfully delete mail (uid %s)'%kargs['uids']
		else:
			raise Exception('Message failed to be delete: '+response)
	
	def create_folder(self,**kargs):
		'''create folder by value of current time: Year/Month/Day/Hour/Min/Sec, layer by layer once a time'''
		todysFolder = datetime.datetime.now().strftime('Year%Y/Month%m/Day%d/Hour%H/Min%M/Sec%S')
		fullpathfolder = self.list_folder(checkfolder=todysFolder, findParent = True)
		kargs['parent'] = fullpathfolder[0]
		if not kargs.has_key('name') or (not kargs['name']):
			kargs['name'] = fullpathfolder[1] 
		#if kargs.has_key('specialDataName'): # for specialDataLib calling
		#	return self.common.request_send(RequestLib.foldercreatereq,kargs,getRes=True)
		#else:
		response = self.common.request_send(RequestLib.foldercreatereq,kargs)
		if fullpathfolder[1] in response:
			return 'checked created folder: '+str(kargs)

	def rename_folder(self, **kargs):
		'''Rename the first valid user created folder to default folder '''
		folder = {}
		folder['source'] = self._findFirstUserFolder()
		if kargs.has_key('target'):
			folder['target'] = str(kargs['target']) # folder['source'] 
			print folder['target']
		else:
				folder['target'] = folder['source'] + 'Renamed'
		#if kargs.has_key('specialDataName'): # for specialDataLib calling
		#	return self.common.request_send(RequestLib.folderrename, folder, getRes=True)
		renameFolderRes = self.common.request_send(RequestLib.folderrename,folder)
		if '<status>ok</status>' in renameFolderRes:
			return 'Successfully rename folder from %s to %s'%(folder['source'],folder['target'])
		else:
			raise Exception('Failed to rename folder')

	def move_folder(self,**kargs):
		'''Move the first valid user created folder to default folder - ${mail_folderMoveTo} '''
		foldersResp = self.list_folder()
		fullnameList = re.findall('<folder name=".*" fullname="(.*)" msgcount', foldersResp.replace('><','>\n<'))
		print 'folder(s): '+str(fullnameList)
		failedLog = ''
		for folder in fullnameList:
			if '/' in folder or folder in ['INBOX', 'Inbox', 'Drafts', 'Sent', 'spam', 'Spam', 'Trash','SentMail']:
				pass
			else:
				kargs['source'] = folder
				moveFolderRes = self.common.request_send(RequestLib.foldermove,kargs)
				if 'Trash/%s'%folder not in moveFolderRes:
					failedLog = failedLog + '%s not in removed response,\n'%folder
				if not kargs.has_key('all'):
					break
		if failedLog:
			raise Exception('There is no valid folder could be removed')
		else:
			return 'Folder(s) moved!'

	def delete_folder(self):
		'''Delete the first mail from Trash folder'''
		kargs = {}
		kargs['name'] = 'Trash/'+self._findFirstUserFolder(fromTrash=True)
		if kargs['name'] == 'no valid folder':
			raise Exception('There is no valid folder in trash could be delete')
		else:
			delFolderRes = self.common.request_send(RequestLib.folderdelete,kargs)
			if '<status>ok</status>' in delFolderRes:
				return 'Successfully delete folder %s'%(kargs['name'])
			else:
				raise Exception('Failed to delete folder') 
		
	def empty_folder(self,**kargs):
		# trashFolder = 'Trash/'+self._findFirstUserFolder(fromTrash=True)
		# if trashFolder == 'no valid folder':
			# raise Exception('There is no valid folder in trash could be delete')
		# else:
		emptyFolderRes = self.common.request_send(RequestLib.folderempty, kargs)
		if '<mail action="folderempty">' in emptyFolderRes and '<status>ok</status>' in emptyFolderRes:
			return 'Successfully empty trash folder'
		else:
			raise Exception('Failed to empty trash folder') 	
			
	def list_blocksenders(self):
		response = self.common.request_send(RequestLib.blockedsenderList)
		if '<blockedsender action="load">' not in response:
			raise Exception('Failed to load block senders')
		else:
			self.bsL = re.findall('.*<sender email="(.*).*" />',response.replace('><','>\n<'))
			return self.bsL
					
	def add_block_sender(self,**kargs):
		'''Only send block sender request, not check it'''
		request = RequestLib.blockedsenderModify%kargs['sender']
		response = self.common.request_send(request)
		if '<blockedsender action="modify" />' in response:
			return 'Add block sender OK!'
		else:
			raise Exception('Failed to add block sender')
		
	def remove_blocksenders(self,**kargs):
		'''	kargs['all'] -> remove all blocked senders'''
		remove = ''
		for sender in self.bsL:
			remove = remove + '<remove>%s</remove>'%sender
			if not kargs.has_key('all'):
				break
		response = self.common.request_send(RequestLib.blocksender_remove%remove)
		if not '<blockedsender action="modify" />' in response:
			raise Exception('Failed to remove blocksender(s)')
		else:
			return 'Removed block sender(s) '+remove
		
	def add_safe_sender(self,**kargs):
		request = RequestLib.safesender_add%kargs['sender']
		response = self.common.request_send(request)
		if '<allowedsender action="modify" />' in response:
			return 'Add safe sender OK!'
		else:
			raise Exception('Failed to add safe sender')
		
	def list_safesenders(self):
		response = self.common.request_send(RequestLib.sefesenderList)
		if '<allowedsender action="load">' not in response:
			raise Exception('Failed to load safe senders')
		else:
			self.ssdL = re.findall('.*<sender email="(.*)" />.*',response.replace('><','>\n<'))
			return self.ssdL
		
	def remove_safesenders(self,**kargs):
		'''	kargs['all'] -> remove all safe senders'''
		remove = ''
		for sender in self.ssdL:
			remove = remove + '<remove>%s</remove>'%sender
			if not kargs.has_key('all'):
				break
		response = self.common.request_send(RequestLib.safesender_remove%remove)
		if not '<allowedsender action="modify" />' in response:
			raise Exception('Failed to remove safesender(s)')
		else:
			return 'Removed safe sender(s) '+remove
		
	def set_signature(self,**kargs):
		''' Two requests:
			1. set signature - kargs['type'], kargs['isdefault'], 
			2. save signature position - kargs['position']=below or above
		'''
		if kargs['type'] == 'html':
			kargs['contentType'] = 'text/html'
			kargs['text'] = '&lt;div style=&quot;text-align: center;&quot;&gt;&lt;b&gt;&lt;u&gt;&lt;font size=&quot;4&quot;&gt;&lt;font color=&quot;#9900ff&quot;&gt;this is my rich signatu&lt;/font&gt;re&lt;/font&gt;&lt;/u&gt;&lt;/b&gt;&lt;/div&gt;'
			kargs['label'] = '&lt;div style=&quot;text-align: center;&quot;&gt;&lt;b&gt;&lt;u&gt;&lt;font size=&quot;4&quot;&gt;&lt;font color=&quot;#9900ff&quot;&gt;this is my rich signatu&lt;/font&gt;re&lt;/font&gt;&lt;/u&gt;&lt;/b&gt;&lt;/div&gt;'
		else:
			kargs['contentType'] = 'text/plain'
		if not kargs.has_key('text'):
			kargs['text'] = 'this is my plain signaure'
		if not kargs.has_key('label'):
			kargs['label'] = 'this is my plain signaure label'
		
		signatureReq = self.common.request_send(RequestLib.mailSignature, kargs,getRes=True)
		# if kargs.has_key('specialDataName'): # for specialDataLib calling
			# return signatureReq
		
		self.signaureKW = signatureReq.split('label="')[1].split('"')[0]
		signatureResp = self.common.request_send(signatureReq)
		if self.signaureKW in signatureResp:
			pass
		else:
			raise Exception('Signature %s not setted'%self.signaureKW)
			
		positionReq = RequestLib.signaturePosition%kargs['position']
		positionResp = self.common.request_send(positionReq)
		if '<prefs action="set" />' in positionResp:
			return 'Signature created (%s)(%s)'%(self.signaureKW,kargs['position'])
		else:
			raise Exception('Signature position failed to be setted')
		
	def delete_signature(self):
		id = self.listSignatureId(listFirst=True)
		response = self.common.request_send(RequestLib.mailSignatureDelete%id)
		if '<mailSignature action="delete" />' in response:
			return 'First Signature (id:%s)has been successfully deleted'%id
		else:
			raise Exception('Signature failed to be deleted')
		
	def auto_forward(self,**kargs):
		print '+++++++++++++++++++++++++++++++'
		print RequestLib.mailForwarding
		print kargs
		autoFwdReq = self.common.request_send(RequestLib.mailForwarding, kargs)
		if 'destination="' + kargs['email']:
			return 'Set auto forward to '+kargs['email']
		else:
			raise Exception('Failed to Set auto forward to '+kargs['email'])
	
	def get_mail_prefs(self,expect=False):
		self.getprefs = self.common.request_send(RequestLib.prefsGet)
		if expect:
			if expect in self.getprefs:
				return 'Sueccesfully set prefs: '+expect
			else:
				raise Exception('Failed to set prefs: '+expect)
		else:
			return self.getprefs
		
	def set_mail_prefs(self,**kargs):
		'''kargs['setDefault'] -> pre-steps: set default prefs 
			'''
		defaultReq = RequestLib.prefsSet_mail
		if kargs.has_key('setDefault'):
			defaultPrefsResponse = self.common.request_send(defaultReq)
			if '<prefs action="set" />' in defaultPrefsResponse:
				return 'Set default prefs Successfull!' + defaultReq.split('<prefs action="set">')[1].split('</prefs></request>')[0]
			else:
				raise Exception('Failed to set default: '+defaultReq.split('<prefs action="set">')[1].split('</prefs></request>')[0])
		
		else:
			newReq = self._setPrefValue(defaultReq,kargs['prefsName'], kargs['prefsValue'])
			response = self.common.request_send(newReq)
			return self.get_mail_prefs(expect='<pref name="%s">%s</pref>'%(kargs['prefsName'],kargs['prefsValue']))
		
	def outgoing_checkinverval_replyquote(self,**kargs):
		'''default is saveOutgoingMessages="true" autoCheckInterval="1800" replyQuoting="false"'''
		if not kargs.has_key('saveOutgoingMessages'):
			kargs['saveOutgoingMessages'] = 'false'
		if not kargs.has_key('autoCheckInterval'):
			kargs['autoCheckInterval'] = '0'	
		if not kargs.has_key('replyQuoting'):
			kargs['replyQuoting'] = 'false'	
		
		defaultPrefsResp = self.common.request_send(RequestLib.saveOutgoingMessages, kargs)
		faillog = ''
		for item in kargs:
			if '%s="%s"'%(item,kargs[item]) in defaultPrefsResp:
				pass
			else:
				faillog = faillog + item +', '
		if faillog:
			raise Exception('Failed to set prefs: ' + faillog)
		else:
			return 'Successfully set prefs: ' + str(kargs)

	def add_external_account(self,**kargs):
		'''
			Two requests: 
				1. mail action="testexternalaccountconnection
				2. smailExternalAccount action="create"
			Kargs:
				name - external account whole address
				psw - password of external account
			'''
		# externalName = kargs['name']
		# externalPsw = kargs['psw']	
		# accountDetail = RequestLib.externalmailaccount%(externalPsw,externalName,externalName,externalName,externalName)
		# mailAction_testConn = '<mail action="testexternalaccountconnection">' + accountDetail + '</mail>'
		# mailExternalAccount_create = '<mailExternalAccount action="create">' + accountDetail + '</mailExternalAccount>'
		
		getConnectResp = self.common.request_send(RequestLib.externalmailaccount_test, kargs)
		if '<success />' in getConnectResp:
			pass
		else:
			raise Exception('Failed to connect to external account')
			
		createAccountResp = self.common.request_send(RequestLib.externalmailaccount, kargs)
		self.createRespPiece = createAccountResp.split('accountName=')[1].split('checkOnStartup')[0]
		return self.createRespPiece + '...'

	def empty_external_account(self, **kargs):
		accountListResp = self.common.request_send(RequestLib.externalAccountList)
		print accountListResp

				
	def check_external_account(self, **kargs):
		'''Kargs:
				name - external account whole address
				psw - password of external account
				checkDulp - if duplicate, then delete the account'''
				
		accountListResp = self.common.request_send(RequestLib.externalAccountList)
		if kargs.has_key('checkDup'):
			if kargs['name'] in accountListResp:
				id = accountListResp.split('externalmailaccount id="')[1].split('"')[0]
				return self._removeExternalAccount(id)
			else:
				return kargs['name'] + ' not exist yet'
				
		else:
			if self.createRespPiece in accountListResp:
				return 'Checked account: ' + self.createRespPiece
			else:
				raise Exception('Account not in mailExternalAccount list')

	def enable_disposable_address(self, **kargs):
		'''	http://172.20.0.79:8081/mxos/mailbox/v2/webtop6@openwave.com/base/
			maxNumAliases=10'''
		url='http://172.20.0.79:8081/mxos/mailbox/v2/webtop6@openwave.com/base/'
		self.common.simple_post(url, kargs)
				
	def add_disposable_address(self, **kargs):
		'''	kargs['domain'] for the fake address domain
			fakeAddrName=1_h17m48s01    preferredName=name1_h17m48s01'''
		for i in range(int(kargs['n'])):
			fakeAddrName = str(i+1)+'_'+datetime.datetime.now().strftime('h%Hm%Ms%S')
			address = fakeAddrName+kargs['domain']
			preferredName = 'name'+fakeAddrName
				
			resp = self.common.request_send(RequestLib.mailAlias_add%(address, preferredName))
			failedLog = ''
			if 'name="%s"'%address in resp and 'preferredName="%s"'%preferredName in resp:
				pass
			else:
				failedLog = failedLog+address+'_'+preferredName+'\n'
		if failedLog:
			raise Exception('Failed to get correct respose for ADD a disposable address: '+failedLog)
		else:
			return 'Disposable address(es) created!'
	
	def list_disposable_address(self):
		resp = self.common.request_send(RequestLib.mailAlias_list)
		if '<mailAlias action="list">' in resp:
			self.address_name_list = re.findall('.*<mailalias .* name="(.*)" .* preferredName="(.*)" notes=".*" />.*', resp.replace('><','>\n<'))
			print 'Disposable address&name list is '+str(self.address_name_list)
			return self.address_name_list
		else:
			raise Exception('Failed to list desposable address')
			
	def delete_disposable_address(self, **kargs):
		failedLog = ''
		for contact in self.address_name_list:
			resp = self.common.request_send(RequestLib.mailAlias_delete%contact[0])
			if '<mailAlias action="delete" />' not in resp:
				failedLog = failedLog + contact[1] + '\n'
			if not kargs.has_key('all'):
				break
			
		if failedLog:
			raise Exception('Failed to delete the disposable address(es)\n'+failedLog)
		else:
			return 'Successfully deleted disposable address(es)'
		
	def enable_auto_reply(self, **kargs):
		'''	kargs: 
			kargs['otherdomains'] -> Send a different response to emails from specific domains, like example.com, company.com. 
			kargs['needsetmore'] -> only auto reply message without any other settings
			basic auto reply settings is only keep reply content, all others are False'''
		self.useraddress = CommonLib.CommonLib.useraddress
		self.name = self.useraddress.split('@')[0]
		if kargs.has_key('otherdomains'):
			request = RequestLib.autoReply%(self.name,'myexample.com, mycompany.com', 'this is message from the other domain')
		else:
			request = RequestLib.autoReply%(self.name,'','')
		if kargs.has_key('needsetmore'):
			self.autoReply = WebtopResponseWrap.WebtopResponseWrap(request)
			return 'Auto reply basic setting object is ready'
		else:
			resp = self.common.request_send(request)
			kw = 'vacationmessage enabled="true" message="%s"'%request.split('message="')[1].split('"')[0]
			if kw in resp:
				return 'Auto reply ENABLED with the basic reply content'
			else:
				raise Exception('Auto reply FAILed to be enabled with the basic reply content')
		
	def set_auto_reply(self, **kargs):
		if kargs.has_key('original'):
			self.autoReply.setElementValue(xPath='mailVacationMessage/vacationmessage', valueText='', attrib={'original':'true'})
			# self.autoReply.addElement(xPath= 'mailVacationMessage/vacationmessage/options', tag='option', attrib={'name':'vactionMode','value':'true'}, valueText='')
			self.autoReply.addElement(xPath= 'mailVacationMessage/vacationmessage/options', tag='option', attrib={'name':'attachOriginalMessageToReply','value':'true'}, valueText='')
		if kargs.has_key('replyonce'):
			self.autoReply.setElementValue(xPath='mailVacationMessage/vacationmessage', valueText='', attrib={'replyOnce':'true'})
		if kargs.has_key('freqInterval'):
			self.autoReply.setElementValue(xPath='mailVacationMessage/vacationmessage', valueText='', attrib={'frequency':'on','interval':kargs['freqInterval']})
		
		
		print self.autoReply.toXML()
		resp = self.common.request_send(self.autoReply.toXML())
		return resp
	
	def save_image_blocker(self, **kargs):
		'''	kargs['method'] '''
		r={}
		r['0'] = 'Always allow images'
		r['1'] = 'Always block images'
		r['2'] = 'Always allow images from contacts in address book'
		r['3'] = 'Always allow images except when tagged as spam or in spam folder'
			
		resp = self.common.request_send(RequestLib.imageBlocker%kargs['method'])
		if '<imageBlocker action="save" />' in resp:
			return 'Image blocker saved '+r[kargs['method']]
		else:
			raise Exception('Failed to save block sender')
			
	def trust_image_sender(self, **kargs):
		'''	kargs['trust'] - trust img sender for 'Always block images'	'''
		resp = self.common.request_send(RequestLib.trustImgSender%kargs['trust'])
		if 'address="%s"'%kargs['trust'] in resp:
			return 'Add a trust sender: '+kargs['trust']
		else:
			raise Exception('Failed to add a trust sender: '+kargs['trust'])
		
	def image_trust_list(self, **kargs):
		''' kargs['senders'] = addrsses divided by space'''
		resp = self.common.request_send(RequestLib.imgTrustList)
		self.imgTrustId = re.findall('.*<trustedsender id="(.*)" address=".*" />.*', resp.replace('><','>\n<'))
		self.imgTrustSender = re.findall('.*<trustedsender id=".*" address="(.*)" />.*', resp.replace('><','>\n<'))
		if kargs['sender'] not in self.imgTrustSender:
			raise Exception(str(kargs['sender'])+' is NOT found in trust list')
		else:
			return str(kargs['sender'])+' is found in trust list'
		
	def delete_img_trust_sender(self,**kargs):
		'''	kargs['all'] - delete all senders in the list'''
		idxml = ''
		for id in self.imgTrustId:
			if not kargs.has_key('all'):
				break
			idxml = idxml + '<id>%s</id>'%id
		resp = self.common.request_send(RequestLib.imgtrustSender_delete%idxml)
		if '<trustedsender action="delete" />' in resp:
			ids = idxml.split('</id>')
			print 'Deleted below trust sender(s): '
			return ids
		else:
			raise Exception('Failed to delete trust sender')
		
	def remove_All_Singature(self, **kargs):
		ids = self.listSignatureId()
		request_str = RequestLib.signature_delete_cntr
		id_nodes = ''
		for id in ids:
			id_nodes = id_nodes + RequestLib.signature_id_node%id
		
		request_str = request_str%id_nodes
		response = self.common.request_send(request_str)
		if '<mailSignature action="delete" />' in response:
			return 'All Signatures have been successfully deleted'
		else:
			raise Exception('Signature failed to be deleted')		

	def create_MaxCnt_Signature(self, **kargs):
		if not kargs['maxCnt']:
			raise Exception('not maxCount parameter found!')
		if kargs['maxCnt'] <= 0:
			raise Exception('input parameter maxCount is invalid!')
		maxCount = int(kargs['maxCnt']) + 2#one for range,one for more than max count
		for i in range(1,maxCount):
			try:
				kargs['type'] = 'text'
				kargs['label'] = str(i)
				kargs['contentType'] = 'text/plain'
				kargs['text'] = 'this is my plain signaure'
				kargs['position'] = 'below'
				kargs['isDefault'] = 'false'
				res = self.set_signature(**kargs)
			except Exception,e:
				if i == (maxCount - 1):#need to assert the error code
					return 'case passed!'
				else:
					raise e
		raise Exception("Max Signature Count config doesn't work!")	

	def create_single_folder(self,**kargs):
		response = self.common.request_send(RequestLib.foldercreatereq,kargs)
		print response
		if kargs['name'] in response:
			return 'checked created folder: '+str(kargs)
		else:
			raise Exception('cant create folder %s'%kargs['name'])
		
	def create_MaxNestedLayer_Folder(self, **kargs):
		if not kargs.has_key('folderDepth'):
			raise Exception('Missing maxDepth in parameters!')
		folderDepth = int(kargs['folderDepth']) + 1
		parentName = ''
		for depth in range(1, folderDepth + 1):
			try:
				params = {}
				params['parent'] = parentName
				params['name'] = 'zzmaxfolder' + str(depth)
				self.create_single_folder(**params)
				if parentName == '':
					parentName = params['name']
				else:
					parentName = parentName + '/' + params['name']
			except Exception,ex:
				if (depth == folderDepth):#to do:need to assert the error msg
					return 'case pass!'
				else:
					raise Exception('Fail to create %s layer folder, the max nested layer is %s! %s'%(depth, kargs['folderDepth'], ex))

		raise Exception('Exceed the nested layer limitation %s! No error found in response.'%kargs['folderDepth'])

	def sort_Mail_By_Subject(self, **kargs):
		#send to sort requets
		kargs['sortby'] = 'subject'
		response = self.common.request_send(RequestLib.msgheaderlist_sort, kargs)
		sortedL = re.findall('<msg uid=".*" subject="(.*)" seen=', response.replace('><','>\n<'))
		#send list request
		expectsortL = copy.copy(sortedL)
		if kargs['sortorder'] == 'ASC':
			#expectsortL.sort()
			#sorted(expectsortL, key=str.encode('UTF-8').lower)
			sorted(expectsortL, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()))
		else:
			sorted(expectsortL, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()), reverse=True)
		
		if sortedL == expectsortL:
			return ' correctly sorted with ' + kargs['sortorder']
		else:
			raise Exception('Not correctly sorted')

	def sort_Mail_By_Date(self, **kargs):
		#send to sort requets
		kargs['sortby'] = 'date'
		response = self.common.request_send(RequestLib.msgheaderlist_sort, kargs)
		#get timestamp
		sortedL = re.findall('sent-date="[0-9]+" received-date="([0-9]+)" local-sent-date=".*"', response.replace('><','>\n<'))
		#send list request
		expectsortL = copy.copy(sortedL)
		if kargs['sortorder'] == 'ASC':
			sorted(expectsortL)
		else:
			sorted(expectsortL, reverse=True)
		
		if sortedL == expectsortL:
			return ' correctly sorted with ' + kargs['sortorder']
		else:
			raise Exception('Not correctly sorted')

	def sort_Mail_By_From(self, **kargs):
		#send to sort requets
		#sort by email field(from michael)
		kargs['sortby'] = 'from'
		response = self.common.request_send(RequestLib.msgheaderlist_sort, kargs)
		sortedL_email = re.findall('<from name=".*" address=(.*)', response.replace('><','>\n<'))
		#send list request
		expectsortL = []
		if kargs['sortorder'] == 'ASC':
			expectsortL = sorted(sortedL_email, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()))
		else:
			expectsortL = sorted(sortedL_email, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()), reverse=True)
		if sortedL_email == expectsortL:
			return ' correctly sorted with ' + kargs['sortorder']
		else:
			raise Exception('Not correctly sorted')			

	def create_folder_for_search(self,**kargs):
		response = self.common.request_send(RequestLib.foldercreatereq, kargs)
		if kargs['name'] in response:
			return 'checked created folder: '+str(kargs)
			
	def mail_advanced_search(self, **kargs):
		print kargs
		expectedCnt = int(kargs['expectedCnt'])
		searchResp = self.common.request_send(RequestLib.vmsgheaderlistadvanced, kargs)
		searchStr = '<msg folder="%s'%kargs['folders']
		msg_list = re.findall(searchStr, searchResp.replace('><','>\n<'))
		if len(msg_list) == expectedCnt:
			pass
		else:
			raise Exception('%s mail expected, but %s returns.'%(expectedCnt, len(msg_list)))
		
	def send_msg_for_search(self,**kargs):
		response = self.common.request_send(RequestLib.msgsendRequest_search,kargs)
		return response

	def send_msg_for_receipt(self,**kargs):
		response = self.common.request_send(RequestLib.msgsendRequest_receipt,kargs)
		if not re.search('ok', response):
			raise Exception('send mail failed!')
			
	def check_msg_subject_cnt(self,**kargs):
		expectCnt = int(kargs['expectCnt'])
		searchResp = self.common.request_send(RequestLib.msgheaderlist_receipt, kargs)
		#cannot check count now, because another bug
		#maillst = re.findall('<msg', searchResp)
		#if len(maillst) != expectCnt:
		#	raise Exception('%s mail expected, but %s returns.'%(expectCnt, len(maillst)))
		if expectCnt == 0:
			return
		subjectStr = kargs['subjectStr']
		if not re.search(subjectStr, searchResp):
			raise Exception('Didn\'t find the expected mail(mail subject: %s).'%subjectStr)

	def check_read_receipt_msg(self,**kargs):
		expectCnt = int(kargs['expectCnt'])
		response = self.common.request_send(RequestLib.msgheaderlist%kargs['folder'])
		if (expectCnt == 0) and (not re.search('msg uid', response)):
			return '%s is empty.'%kargs['folder']
		kargs['uid']  = self.common.check_response(getID='uid')
		msgFetchResp = self.common.request_send(RequestLib.msgfetchRequest,kargs)
		maillst = re.findall('<msg', msgFetchResp)
		if len(maillst) != expectCnt:
			raise Exception('%s mail expected, but %s returns.'%(expectCnt, len(maillst)))
		if expectCnt == 0:
			return 'no receipt'
		if not re.search('returnReceipt="%s"'%kargs['receiptVal'], msgFetchResp):
			raise Exception('Didn\'t find returnReceipt field in response.')
		return re.findall('msg uid="([0-9]+)" ', msgFetchResp)[0]
		
	def send_receipt(self, **kargs):
		response = self.common.request_send(RequestLib.msgSendReceipt,kargs)
		return response
		
	def ignore_receipt(self, **kargs):
		response = self.common.request_send(RequestLib.msgIgnoreReceipt,kargs)
		return response
		
	def test_external_account(self, **kargs):
		try:
			response = self.common.request_send(RequestLib.externalmailaccount_test,kargs)
			if re.search('error code', response):
				raise Exception('Cannot connect to external account:%s'%kargs['accountEmail'])
			return 'Connected.'
		except Exception,e:
			raise Exception(e.message)

	def get_external_account_id(self, **kargs):
		accountListResp = self.common.request_send(RequestLib.externalAccountList)
		ids = re.findall('<externalmailaccount id="([0-9a-z-]*)" username="%s"'%kargs['name'], accountListResp)
		return ids[0]

#-----time zone--------
	def get_hk_timestamp(self,**kargs):
		self.prefs = PrefsLib.PrefsLib(self.url)
		
		exec "self.timestamp = self.prefs.get_field_value(response=self.%s, fieldName=kargs['stampName'])"%kargs['response'] #'sent-date'
		return 'first mail from %s is %s'%(kargs['folder'], self.timestamp)
	
	def expt_all_timezones(self,**kargs):
		timezones = self.prefs.list_timezones()
		self.send_tzExp = self.prefs.return_locals_expect(hkTimeStamp= float(self.timestamp), checkFormat=kargs['format'], timezones=timezones)
		return 'Expectations are ready'
		
	def check_time_zones(self,**kargs):
		''' kargs['fieldName'] - actual field name from response'''
		failLog = ''
		print 'checking timezones...'
		for zone in self.send_tzExp:
			self.prefs.set_timezones(specific=zone['name'])
			exec "self.%s(**kargs)"%kargs['function']
			exec "gotTimeField = self.prefs.get_field_value(response=self.%s, fieldName=kargs['fieldName'])"%kargs['response']
			
			if not str(zone['expTime']) in gotTimeField:
				if abs(int(zone['expTime'].split('T')[1]) - int(gotTimeField.split('T')[1])) < 5000:
					pass
				else:
					failLog = failLog + '[%s] %s expect %s, but got %s \n'%(zone['name'], kargs['fieldName'], str(zone['expTime']), gotTimeField)
		if failLog:
			raise Exception(failLog)
		return 'All time zones checked successfully.\n'
	
	def check_hk_time(self, **kargs):
		if not self.prefs:
			self.prefs = PrefsLib.PrefsLib(self.url)
		exec "gotTime = self.prefs.get_field_value(response=self.%s, fieldName=kargs['fieldName'])"%kargs['response']

		gotDateTime = datetime.datetime.strptime(gotTime, kargs['format'])
		timedelta = (datetime.datetime.now()-gotDateTime).seconds
		print 'time delta is '+str(timedelta/60)
		if not timedelta < 15*60: # gap is in 15mins
			print 'time delta is %s mins'%str(timedelta/60)
			raise Exception('Gap on %s between PC local time and response is longer than 30mins'%kargs['fieldName'])
		return 'HK time is correnctly checked on '+kargs['fieldName']

#-----performance-------
	def block_senders(self,**kargs):
		'''domain=${common_domain}	n=250'''
		blocked = 'contact'
		for i in range(int(kargs['n'])):
			h={'sender':blocked+str(i+301)+kargs['domain']}
			self.block_sender(**h)
		return 'set ' + kargs['n']
		
	def request_rateSender(self, **kargs):
		''' kargs['amount']: request amount '''
		requestL = []
		self.e = ''
		request = '<request><mail action="msgheaderlist" accountId="" folder="INBOX" sortby="date" sortorder="desc" count="5" start="0" limit="5"></mail></request>'
		amount = int(kargs['amount'])
		print 'Sending %s requests...'%kargs['amount']
		for i in range(amount):
			requestL.append(request)
		
		self.pool = Pool(amount)
		self.start_time = time.time()
		try:
			results = self.pool.map(self.common.request_send, requestL)
		except Exception, e:
			if kargs.has_key('raiseError'): # response should not contain error code in regular request
				raise Exception(e)
			else:
				self.e = e.message
				return 'Error is: '+ self.e
			
	def request_rateLimiter(self, **kargs):	
		''' kargs['ms']: time limit for requests	'''
		duration_time = time.time() - self.start_time
		# self.pool.close()
		# self.pool.join()
		print 'duration is '+str(duration_time)
		if duration_time > float(kargs['ms'])/1000:
			raise Exception('timeout for requests, need network and server assurance')
		
		else:
			if 'INVALID_REQUEST' in self.e: # expect the correct exception when exceed
				return 'got INVALID_REQUEST for exceed requests exception raised by Request Throttling' # exceed request mount
			else:
				# print self.e
				raise Exception('Need INVALID_REQUEST for exceed requests exception raised by Request Throttling')
		
	def block_duration(self, **kargs):
		kargs['amount'] = 1
		self.request_rateSender(**kargs)
		if 'INVALID_REQUEST' in self.e:  # expect the correct requests when exceed
			print 'got INVALID_REQUEST for exceed requests exception raised by Request Throttling' # exceed request mount
		else:
			print self.e
			raise Exception('Need INVALID_REQUEST for exceed requests exception raised by Request Throttling')
		
		print 'seelp for %s sec'%kargs['duration']
		time.sleep(int(kargs['duration']))
		kargs['raiseError'] = 'true'
		self.request_rateSender(**kargs) # send a regular request
		return 'Request is sent after sleep'

	def change_pwd(self, **kargs):
		response = self.common.request_send(RequestLib.mailpwdchange, kargs)
		if 'ok' in response:
			return 'password changed.'
		else:
			raise Exception('change password failed!')
	
	def set_empty_folder_logout(self, **kargs):
		response = self.common.request_send(RequestLib.mail_empty_trash_logout%kargs['emptyTrashOnLogout'])
	
	def list_mail_by_folder(self, **kargs):
		res = self.common.request_send(RequestLib.msgheaderlist%kargs['folder'])
		msglist = re.findall('<msg uid=', res)
		return len(msglist)
	'''
	def list_attachments(self, **kargs):
		res = self.common.request_send(RequestLib.mail_list_all_attachment%kargs['folder'])
		print res
	
	def get_more_attachments_info(self, **kargs):
		res = self.common.request_send(RequestLib.mail_list_attachment_more%kargs['token'])
		print res
	'''
# if __name__=='__main__':
	# print 'mail lib name space'
	# print user_login(username='username',password='password')
