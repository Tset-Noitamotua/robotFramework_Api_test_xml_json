import datetime, re, os, sys, time, datetime, copy, requests, cgi, platform, json
import xml.etree.ElementTree as ET
import WebtopResponseWrap, Upload, SysUtils #PrefsLib,
sys.path.append(os.path.join('..', 'util'))
''' 
if 'indows' in platform.system():
	sys.path.append('..\util')
else:
	sys.path.append('../util')
'''
#from ImpLibs import consts, utils, reqbuilder, msgconsts
from ImpLibs import *
from Mail import Mail
from TestCodeException import TestCodeException
import SysUtils

class MailLib(Mail):
	''' 
	kargs key from config resource must be exactly same as request attribute name
	'''

	def __init__(self,url):
		Mail.__init__(self, url)
		self.prefs = ''
		self.url = url

	def get_mail_id_by_subject(self, **kargs):
		'''
		use msgheaderlist to find id
		input: folder, subject
		output: a mail id or exception
		'''
		mail_subject = kargs['subject']
		kargs.pop('subject')
		res = self.list_mail(**kargs)
		result_list = utils.getMailIDListBySubject(mail_subject, res)
		if len(result_list) > 1:
			raise Exception('More than 1 mail with subject %s'%mail_subject)
		if len(result_list) < 1:
			raise Exception('Can not find mail with subject %s'%mail_subject)
		return result_list[0]

	def __search_mail_by_subject(self, **kargs):
		'''
		use vmsgheaderlist to search mail
		input: folder, subject
		output: id list
		'''
		res = self.search_mail(**kargs)
		ids = utils.listAll(utils.expr_mail_id, res)
		return ids

	def list_all_mail_id(self,**kargs):
		'''
		input: folder
		output: id list
		'''
		response = self.list_mail(**kargs)
		ids = []
		for mail in json.loads(response)['messages']:
			ids.append(mail['uid'])
		return ids
	
	def get_mail_count_by_folder(self,**kargs):
		id_list = self.list_all_mail_id(**kargs)
		return len(id_list)
	
	def check_message_by_subject(self,**kargs):
		'''
		input: subject, folder, expectCnt
		output: exception or nothing
		'''
		#to do
		expectCnt = -1
		if kargs.has_key('expectCnt'):
			expectCnt = int(kargs['expectCnt'])
			kargs.pop('expectCnt')
		expectSubject = kargs['subject']
		kargs.pop('subject')
		res = self.list_mail(**kargs)
		result_list = utils.getMailIDListBySubject(expectSubject, res)
		if expectCnt != -1:
			if len(result_list) != expectCnt:
				raise Exception('Expect count of mail is %s, but actually got %s'%(expectCnt, len(result_list)))
		return expectSubject
		
	def check_message_by_from_name(self,**kargs):
		'''
		input: from name, folder, expectCnt
		output: exception or nothing
		'''
		name = kargs['name']
		kargs.pop('name')
		expectCnt = -1
		if kargs.has_key('expectCnt'):
			expectCnt = int(kargs['expectCnt'])
			kargs.pop('expectCnt')
		res = self.list_mail(**kargs)
		result_list = utils.getMailListByFromName(name, res)
		if expectCnt != -1:
			if len(result_list) != expectCnt:
				raise Exception('Expect count of mail is %s, but actually got %s'%(expectCnt, len(result_list)))

	def check_mail_flag(self,**kargs):
		flag_name = kargs['flag']
		flag_value = kargs['value']
		mail_id = kargs['id']
		kargs.pop('flag')
		kargs.pop('value')
		kargs.pop('id')
		res = self.list_mail(**kargs)
		flag_actual_value = utils.getFlagValueByMailID(mail_id, flag_name, res)
		if (flag_value == 'False') and (flag_actual_value == None):
			return
		if flag_value != str(flag_actual_value):
			raise Exception('flag mail work incorrectly! %s should be %s, but actually it is %s !'%(flag_name, flag_value, str(flag_actual_value)))

	def check_message_by_str(self,**kargs):
		'''
		input: str, folder, expectCnt
		output: exception or nothing
		'''
		expect_str = kargs['expectStr']
		expect_cnt = -1
		if kargs.has_key('expectCnt'):
			expect_cnt = int(kargs['expectCnt'])
			kargs.pop('expectCnt')
		kargs.pop('expectStr')
		
		res = self.list_mail(**kargs)
		result_list = utils.listAll(expect_str, res)
		if expect_cnt > -1:
			if len(result_list) != expect_cnt:
				raise Exception('Expect count of mail is %s, but actually got %s'%(expect_cnt, len(result_list)))				

	def new_mail_check(self,**kargs):
		expectStr = kargs['expectStr']
		kargs.pop('expectStr')
		res = self.mail_header_list_check(**kargs)
		if not expectStr in res:
			raise Exception('check new mail failed! Did not find the new mail with str(%s)'%expectStr)

	def check_message_fetch_by_subject(self,**kargs):
		''' input: uid=${mail id}'''
		expect_list = kargs['expectStr'].split(',')
		kargs.pop('expectStr')
		fetch_response = self.msg_fetch(**kargs)
		print fetch_response
		for expect in expect_list:
			if expect not in fetch_response:
				raise Exception('Expect (%s) not in res(%s)'%(expect, fetch_response))	

	def _findFirstUserFolder(self, fromTrash=False):
		folderList = self.list_folder()
		try:
			if fromTrash:
				trashFolder = utils.listALLItem(utils.expr_trash_folder_id, folderList)
				if len(trashFolder) > 0:
					return trashFolder[0]
				else:
					return 'no valid folder'
			else:
				fullnamefolderL = utils.listALLItem(utils.expr_folder_id,folderList)
				for fullNameFolder in fullnamefolderL:
					if fullNameFolder not in ['INBOX', 'Drafts', 'Sent', 'spam', 'Spam', 'Trash','SentMail']:
						return fullNameFolder
					else:
						deleteFolder = 'no valid folder'
						pass
		except Exception,e:
			raise Exception(e)
	
	def listSignatureId(self, listFirst=False):
		listSignatureRes = self.list_signature()
		signatureIDs = utils.getSignatureIDList(listSignatureRes)
		if listFirst:
			if len(signatureIDs) > 0 :
				raise Exception('No signature found!')
			return signatureIDs[0]
		else:
			return signatureIDs
	'''
	def list_folder(self,checkfolder='',findParent = False):
		listfolderRes = self.list_folder()
		newfolder = 'test'
		if findParent:
			
			while not utils.isfolderExisted(checkfolder, listfolderRes):
				if '/' in checkfolder:
					print checkfolder.split('/')
					newfolder = checkfolder.split('/')[-1]
					checkfolder = checkfolder.replace('/'+checkfolder.split('/')[-1],'')
				else:
					newfolder = checkfolder
					checkfolder = ''
					#break
			fullpath = [checkfolder,newfolder]
			print fullpath
			return fullpath
		else:
			return listfolderRes
	'''		

	def upload_file_old(self,**kargs):
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
			print '**********************************'
			attach = Upload.uploadResource(self.uploadURL, self.filePath, fileid, fileName = kargs['fname'])
			self.fidL.append(attach['id'])
		self.fids = ','.join(self.fidL)
		print '[files]: ' + kargs['fname'] +'|[file id]: '+ self.fids
		print 'Successfully upload attachments!'
		return self.fids

	def send_with_img(self,**kargs):
		'''
			same kargs as send mail 
			kargs['smileFace']=$self,**kargs{mail_faceImg}, kargs['faceIcon']=1 ~ 49
		'''
		#make a mail body with img
		if ('http:' in kargs['imgurl']):#fusion
			#kargs['body'] = cgi.escape(msgconsts.MAIL_IMG_BODY%kargs['imgurl'])
			kargs['body'] = msgconsts.MAIL_IMG_BODY%kargs['imgurl']
		else:
			kargs['body'] = kargs['imgurl']#otosan &#9829;
		kargs['bodyType'] = 'html'
		kargs.pop('imgurl')
		#send mail
		try:
			res = self.send_mail(**kargs)
			return 'Mail is sent with image body.'
		except Exception, e:
			raise TestCodeException('Send mail with image failed. %s'%str(e))
		
	def check_img_mail(self,**kargs):
		b_block = kargs['block']
		kargs.pop('block')
		imgurl = ''
		if kargs.has_key('imgurl'):
			imgurl = kargs['imgurl']
			kargs.pop('imgurl')
		res = self.msg_fetch(**kargs)
		if (b_block == 'true'):
			print msgconsts.MAIL_BLOCK_IMG
			print res
			if not (msgconsts.MAIL_BLOCK_IMG in res):
				raise Exception('Did not get images blocked!')
		else:
			if imgurl == '':
				raise Exception('Can not find parameter: imgurl !')
			if not (msgconsts.MAIL_IMG_BODY%imgurl in res):
				raise Exception('Expect images not get blocked, but actually blocked!')

	def preview_attachments(self,**kargs):
		'''url=${mail_get_attach_url}	folder=INBOX'''
		url = kargs['url']
		kargs.pop('url')
		ids = self.list_all_mail_id(**kargs)
		print len(ids)
		if len(ids) != 1:
			raise Exception('too many mail found!')
		kargs['messageUid'] = ids[0]
		fetch_response = self.msg_fetch(**kargs)

		attachN = len(re.findall('"part": ',fetch_response))
		print '----------------------------------------'
		print attachN
		failedResult = ''
		for partN in range(attachN):
			print '+++++++++++++++++++++'
			print partN
			print url
			url = url%(kargs['folderPath'],kargs['messageUid'],str(partN+1))
			print '^^^^^^^^^^^^^^^^^^^'
			print url
			sock = Upload.getResource(url)
			print 'previewing...' + str(kargs['messageUid'])
			if str(sock.code) == '200':
				print 'read>>'+str(sock.read(100))
			else:
				failedResult = failedResult + '%s found %s'%(str(partN+1),str(sock.code)) + '\n'
		if failedResult:
			raise Exception('Resource not get %s found!'%str(kargs['messageUid']))
		else:
			return 'All esource succesfully get with HTTP code '+str(sock.code)
	'''		
	def open_message(self,**kargs):
		hostport = ''
		if kargs.has_key('hostport'):
			hostport = kargs['hostport']
			kargs.pop('hostport')
		
		ids = self.list_all_mail_id(**kargs)
		if len(ids) == 0:
			raise Exception('No mail to open!')
		
		#msguid = self.check_response(getID='msg uid')
		url = hostport + consts.saveMailToComputer
		url = url%('', kargs['folderPath'], ids[0]) 
		
		code = Upload.getResource(url).code
		if str(code) == '200':
			return 'GET mail %s .eml'%ids[0]
		else:
			raise Exception('Failed to GET mail %s .eml'%ids[0])
	'''
	def move_all_mail(self,**kargs):
		'''move the first mail from attribute 'folder' to the first valid created folder, then check destination folder list
			dstfolder -> the destination folder name
			all -> move all messages'''
		try:
			move_all = kargs.has_key('all')
			kargs.pop('all')
			ids = self.list_all_mail_id(folderPath=kargs['params.folderPath'])
			print ids
			if move_all:
				kargs['params.selection'] = ids
			else:
				print ids[0:1]
				kargs['params.selection'] = ids[0:1]
			response = self.move_mail(**kargs)
		except Exception, e:
			raise Exception('move_all_mail failed : '%str(e))
	#?
	def save_message_negative(self, **kargs):
		try:
			self.save_draft(**kargs)
		except Exception, e:
			if kargs['errorcode'] not in e.message:
				raise Exception('Expect %s but got %s'%(kargs['errorcode'],e.message))
		
	def print_preview_message(self, **kargs):
		ids = self.list_all_mail_id(**kargs)
		if len(ids) == 0:
			raise Exception('No mail to print priview!')
		
		#uid = self.check_response(getID='msg uid')
		envurl = self.url.replace('/dd','')
		#valid enum values are [none, embeddedOnly, embeddedAndRemote]
		url = envurl +'/bin?r=mail.message.print{accountId:"",folderPath:"%s",messageUid:%s,images:"none"}'%(kargs['folder'],ids[0])
		print 'url is '+url
		
		sock = Upload.getResource(url)
		if str(sock.code) == '200':
			return 'print preview read 100>>'+str(sock.read(100))
		else:
			raise Exception('%s found %s'%(str(partN+1),str(sock.code)))

	def download_message(self, **kargs):#for calendar event mail download.
		ids = self.list_all_mail_id(**kargs)
		if len(ids) == 0:
			raise Exception('No mail to download!')
		
		#uid = self.check_response(getID='msg uid')
		envurl = self.url.replace('/dd','')
		#valid enum values are [none, embeddedOnly, embeddedAndRemote]
		url = envurl +'/http/viewattachment?&accountId&folder=%s&uid=%s&part=1'%(kargs['folder'],ids[0])
		print 'url is '+url
		
		sock = Upload.getResource(url)
		if str(sock.code) == '200':
			return 'download mail read 100>>'+str(sock.read(100))
		else:
			raise Exception('%s found %s'%(str(partN+1),str(sock.code)))

	def check_message_header_subject(self,**kargs):
		'''kargs['folder']'''
		mail_subject = kargs['subject']
		kargs.pop('subject')
		response = self.list_mail(**kargs)
		if mail_subject in response:
			return '%s is checked in %s'%(mail_subject, kargs['folderPath'])
		else:
			raise Exception('%s is NOT in %s'%(mail_subject, kargs['folderPath']))
	#need to refactor
	def search_message(self,**kargs):
		self.vmsgheaderlistResp = self.search_mail(**kargs)#send reqeust should return json obj???
		id_list = utils.getMailIDList(self.vmsgheaderlistResp)
		msg_count = json.loads(self.vmsgheaderlistResp)['messageCount']
		if len(id_list) != msg_count:
			raise Exception('Got % msgs, but messageCount is %s in response!'%(len(id_list), msg_count))
		
		for id in id_list:
			fetch_response = self.msg_fetch(messageUid=id)
			if kargs['params.terms'] in fetch_response:
				return 'Successfully searched mail with %s'%(kargs['params.terms'])
			else:
				raise Exception('Failed to searched mail by '+kargs['params.terms'])	

	def create_folder_positive(self,**kargs):
		res = self.create_folder(**kargs)
		expect_key = ''
		if kargs.has_key('parentPath') and kargs['parentPath'] != '' and kargs['parentPath'] != None:
			expect_key = kargs['parentPath'] + '/'
		if kargs.has_key('name'):
			expect_key = expect_key + kargs['name']
		
		if expect_key  not in res:
			raise Exception('Folder created incorrect!')
			
	def delete_folder_positive(self,**kargs):
		res = self.delete_folder(**kargs)
		result_obj = json.loads(res)
		if result_obj != {}:
			raise Exception('Failed to delete folder %s'%kargs['params.folderPaths'])
			
	def check_folder_existed(self,**kargs):	
		folderFullPath = kargs['fullname']
		kargs.pop('fullname')
		expectCnt = kargs['expectCnt']
		kargs.pop('expectCnt')
		res = self.list_folder(depth=-1)
		result_list = utils.getFolderListByFullName(folderFullPath, res)
		if len(result_list) != int(expectCnt):
			raise Exception('Expect count of folder(%s) is %s, but actually got %s'%(folderFullPath, int(expectCnt), len(result_list)))

	def delete_all_folder(self,**kargs):
		res = self.list_folder()
		name_list = utils.getFolderListFromListRes(res)
		for fullname in name_list:
			if fullname not in msgconsts.SYS_FOLDER:
				try:
					param = {"params.folderPaths" : fullname}
					self.delete_folder_positive(**param)
				except Exception, e:
					if msgconsts.FOLDER_NOT_FOUND not in str(e):
						raise e
			
	def list_blocksenders_id(self, **kargs):
		response = self.list_blocksender(**kargs)
		print response
		if utils.isBlockSenderListed(response):
			return utils.getBlockSenderIDList(response)
		else:
			raise Exception('Failed to load block senders')
	#?				
	def add_block_sender_positive(self,**kargs):
		'''Only send block sender request, not check it'''
		response = self.add_block_sender(**kargs)
		if not utils.isBlockSenderAdded(response):
			raise Exception('Failed to add block sender')
	
	def del_blocksender_positive(self,**kargs):
		response = self.del_blocksender(**kargs)
		if not utils.isBlockSenderAdded(response):
			raise Exception('Failed to remove block sender')
	
	def empty_blocksenders(self,**kargs):
		'''	kargs['all'] -> remove all blocked senders'''
		try:
			res = self.list_blocksender()
			result_obj = json.loads(res)
			sender_list = result_obj["senders"]
			if [] == sender_list:
				return
			res = self.update_blocksender(remove=sender_list)
		except:
			raise Exception('Failed to remove blocksender(s)')

	def check_blocksender_existed(self,**kargs):
		res = self.list_blocksender()
		expectStr = kargs['expectStr']
		for str in expectStr.split(','):
			if not str in res:
				raise Exception('Can not find %s in %s!'%(str, res))

	def check_safesender_existed(self,**kargs):
		res = self.list_safesender()
		expectStr = kargs['expectStr']
		for str in expectStr.split(','):
			if not str in res:
				raise Exception('Can not find %s in %s!'%(str, res))
				
	def list_safesenders_id(self,**kargs):
		response = self.list_safesender(**kargs)
		if utils.isSafeSenderListed(response):
			return utils.getSafeSenderIDList(response)
		else:
			raise Exception('Failed to load block senders')
	
	def empty_safesenders(self,**kargs):
		try:
			res = self.list_safesender()
			result_obj = json.loads(res)
			sender_list = result_obj["senders"]
			if [] == sender_list:
				return
			res = self.update_safesender(remove=sender_list)
		except:
			raise Exception('Failed to remove safesender(s)')	
	
	def del_safesender_positive(self,**kargs):
		response = self.del_safesender(**kargs)
		if not utils.isSafeSenderRemoved(response):
			raise Exception('Failed to remove safe sender')
			
	def get_signature_id_by_label(self,**kargs):
		res = self.list_signature()
		signature_id_list = utils.getSignatureIDByLabel(kargs['label'], res)
		if len(signature_id_list) < 1:
			raise Exception('Did not find signature with label %s'%kargs['label'])
		return signature_id_list[0]

	def create_signature_positive(self,**kargs):
		''' Two requests:
			1. set signature - kargs['type'], kargs['isdefault'], 
			2. save signature position - kargs['position']=below or above
		'''
		if kargs['params.object.contentType'] == 'text/html':
			kargs['params.object.text'] = '&lt;div style=&quot;text-align: center;&quot;&gt;&lt;b&gt;&lt;u&gt;&lt;font size=&quot;4&quot;&gt;&lt;font color=&quot;#9900ff&quot;&gt;this is my rich signatu&lt;/font&gt;re&lt;/font&gt;&lt;/u&gt;&lt;/b&gt;&lt;/div&gt;'
			kargs['params.object.label'] = '&lt;span style=&quot;background-color: rgb(153, 0, 255);&quot;&gt;&lt;b&gt;this is a html signature&lt;/b&gt;&lt;/span&gt;'

		signatureResp = self.create_signature(**kargs)
		if kargs['params.object.label'] in signatureResp:
			pass
		else:
			raise Exception('Signature %s not setted'%kargs['params.object.label'])

	def create_maxsize_signature(self,**kargs):
		try:
			signatureResp = self.create_signature(**kargs)
		except Exception, e:
			if msgconsts.SIGNATURE_TOO_LARGE in str(e):
				return
		raise Exception('Should raise signature too larg exception, but actually not!')

	def list_all_signature_id(self, **kargs):
		res = self.list_signature()
		return utils.getSignatureIDList(res)
	
	def empty_signature(self, **kargs):
		id_list = self.list_all_signature_id()
		print id_list
		if id_list == []:
			return
		try:
			params = {'params.ids' : id_list}
			del_res = self.del_signature(**params)
		except Exception, e:
			raise e
	#?	
	def outgoing_checkinverval_replyquote(self,**kargs):
		'''
		default is saveOutgoingMessages="true" autoCheckInterval="1800" replyQuoting="false"
		'''
		defaultPrefsResp = self.request_send('SAVE_OUTGOING_MSG', **kargs)
		print defaultPrefsResp
		faillog = ''
		for item in kargs:
			print '%s="%s"'%(item,kargs[item])
			if '%s="%s"'%(item,kargs[item]) in defaultPrefsResp:
				pass
			else:
				faillog = faillog + item +', '
		if faillog:
			raise Exception('Failed to set prefs: ' + faillog)
		else:
			return 'Successfully set prefs: ' + str(kargs)

	def test_external_account_succ(self,**kargs):
		try:
			getConnectResp = self.test_external_account(**kargs)
		except Exception, e:
			raise Exception('Failed to connect to external account. %s'%str(e))

	def list_external_account_ids(self,**kargs):
		try:
			accountListResp = self.list_external_account()
			ids = utils.getExternalAccIDs(accountListResp)
			return ids
		except Exception, e:
			raise Exception('Get existed exteral account id list failed!')

	def empty_external_account(self,**kargs):
		'''
		list all account
		delete each one
		'''
		id_to_del = self.list_external_account_ids(**kargs)
		try:
			params = {'params.ids' : id_to_del}
			self.del_external_account(**params)
		except Exception, e:
			raise e

	def check_external_account(self, **kargs):
		'''
		username : 
		expectCnt:
		expectStr:not required
		description:
			check external account by username.
			check howmany account with this username existed
			check expect str existed in the external account
		'''
		username = kargs['username']
		expectCnt = int(kargs['expectCnt'])
		accountListResp = self.list_external_account()
		print '********************************'
		print accountListResp
		external_acc_cont_list = utils.getExternalAccCont(username, accountListResp)
		if len(external_acc_cont_list) != expectCnt:
			raise Exception('Expect to get %s external account, but actually got %s'%(expectCnt, len(external_acc_cont_list)))
		
		if kargs.has_key('expectStr'):
			expectStr = kargs['expectStr']
			expect_list = expectStr.split(',')
			
			for each_external in external_acc_cont_list:
				print '***************************************8'
				print each_external
				for each_str in expect_list:
					if not each_str in each_external:
						raise Exception('Expect str %s in %s, but actually not'%(each_str, each_external))
			
	def list_disposable_address_positive(self, **kargs):
		try:
			resp = self.list_disposable_address(**kargs)
			return utils.getDisposableNameList(resp)
		except Exception, e:
			raise e

	def check_disposable_address(self, **kargs):
		ids = kargs['ids']
		kargs.pop('ids')
		expects = kargs['expectStr'].split(',')
		kargs.pop('expectStr')	
		for id in ids:
			res = self.get_disposable_address(id=id)
			for expect_str in expects:
				if not expect_str in res:
					raise Exception('Can not find expect str: %s in %s'%(expect_str, res))
					
	def get_disposable_id_by_name(self, **kargs):
		expect_name = kargs['name']
		try:
			resp = self.list_disposable_address(**kargs)
			address_list = json.loads(resp)
			for addr in address_list:
				if expect_name == addr['name']:
					return addr['id']
		except:
			raise Exception('Get disposable address id by name(%s) failed !'%expect_name)
		raise Exception('Get disposable address id by name(%s) failed !'%expect_name)
			
	def empty_disposable_address(self, **kargs):
		id_list = kargs['ids']
		try:
			self.del_disposable_address(ids=id_list)
		except Exception, e:
			raise e
		return 'Delete all folder successfully!'

	def trust_image_sender(self, **kargs):
		'''	kargs['trust'] - trust img sender for 'Always block images'	'''
		resp = self.create_img_trust_sender(**kargs)
		if utils.isTrustSenderAdded(kargs['address'], resp):
			return 'Add a trust sender: '+kargs['address']
		else:
			raise Exception('Failed to add a trust sender: ' + kargs['address'])
		
	def check_trust_sender_by_addr(self, **kargs):
		''' kargs['address'] = addrsses divided by space'''
		resp = self.list_img_trust_sender(**kargs)
		result_list = utils.listALLItem(kargs['address'], resp)
		if kargs.has_key('expectCnt'):
			expectCnt = int(kargs['expectCnt'])
			if len(result_list) != expectCnt:
				raise Exception('Expect count of img strust senders is %s, but actually got %s'%(expectCnt, len(result_list)))
			
	def __listImgTrustSenderId(self, listFirst=False):
		res = self.list_img_trust_sender()
		imgSenderIDs = utils.getImgTrustSenderIDList(res)
		if listFirst:
			if len(imgSenderIDs) == 0:
				raise Exception('No img trust sender found!')
			return imgSenderIDs[0]
		else:
			return imgSenderIDs
	#?		
	def empty_img_trust_sender(self,**kargs):
		'''	kargs['all'] - delete all senders in the list'''
		ids = self.__listImgTrustSenderId()
		request_str = consts.IMG_TRUST_SENDER_DEL_CNTR
		id_nodes = ''
		for id in ids:
			id_nodes = id_nodes + consts.IMG_TRUST_SENDER_DEL_ID_NODE%id
		
		request_str = request_str%id_nodes
		try:
			response = self.client.send(request_str)
			print response
		except Exception,e:
			raise Exception('Failed to delete Img trust senders !')
			
	def create_MaxCnt_Signature(self, **kargs):
		if not kargs['maxCnt']:
			raise Exception('not maxCount parameter found!')
		if kargs['maxCnt'] <= 0:
			raise Exception('input parameter maxCount is invalid!')
		maxCount = int(kargs['maxCnt']) + 2#one for range,one for more than max count
		kargs.pop('maxCnt')
		for i in range(1, maxCount):
			try:
				kargs['params.object.label'] = str(i)
				kargs['params.object.contentType'] = 'text/plain'
				kargs['params.object.text'] = 'sig %d'%i 
				kargs['params.object.default'] = 'false'
				res = self.create_signature(**kargs)
			except Exception,e:
				if i == (maxCount - 1):#need to assert the error code
					return 'case passed!'
				else:
					raise e
		raise Exception("Max Signature Count config doesn't work!")

	def create_MaxCnt_external_acc(self, **kargs):
		if not kargs['maxCnt']:
			raise Exception('not maxCount parameter found!')
		if kargs['maxCnt'] <= 0:
			raise Exception('input parameter maxCount is invalid!')
		maxCount = int(kargs['maxCnt']) + 2#one for range,one for more than max count
		kargs.pop('maxCnt')
		external_acc_name = kargs['username']
		kargs.pop('username')
		for i in range(1, maxCount):
			try:
				temp_name = str(i) + external_acc_name#duplicate external account is not allowed
				kargs['params.object.username'] = temp_name
				kargs['params.object.accountName'] = temp_name
				kargs['params.object.accountEmail'] = temp_name
				kargs['params.object.accountFromName'] = temp_name
				res = self.add_external_account(**kargs)
				time.sleep(1)
			except Exception,e:
				if i == (maxCount - 1):#need to assert the error code
					return 'case passed!'
				else:
					raise e
		raise Exception("Max external account Count config doesn't work!")	
		
	def create_single_folder(self,**kargs):
		response = self.create_folder(**kargs)
		print response
		if kargs['name'] in response:
			return 'checked created folder: '+str(kargs)
		else:
			raise Exception('cant create folder %s'%kargs['name'])
		
	def create_MaxNestedLayer_Folder(self, **kargs):
		if not kargs.has_key('folderDepth'):
			raise Exception('Missing maxDepth in parameters!')
		origin_depth = kargs['folderDepth']
		kargs.pop('folderDepth')
		folderDepth = int(origin_depth) + 1
		parentName = ''
		for depth in range(1, folderDepth + 1):
			try:
				params = {}
				params['parentPath'] = parentName
				params['name'] = 'folder' + str(depth)
				self.create_single_folder(**params)
				if parentName == '':
					parentName = params['name']
				else:
					parentName = parentName + '/' + params['name']
			except Exception,ex:
				if (depth == folderDepth):#to do:need to assert the error msg
					return 'case pass!'
				else:
					raise Exception('Fail to create %s layer folder, the max nested layer is %s! %s'%(depth, origin_depth, ex))

		raise Exception('Exceed the nested layer limitation %s! No error found in response.'%origin_depth)

	def sort_Mail_By_Subject(self, **kargs):
		#send to sort requets
		#kargs['sortby'] = 'subject'
		response = self.list_mail(**kargs)
		sortedL = utils.getMailSubjectFromMsgListRes(response)
		#send list request
		expectsortL = copy.copy(sortedL)
		if kargs['params.sort.direction'] == 'ascending':
			#expectsortL.sort()
			#sorted(expectsortL, key=str.encode('UTF-8').lower)
			sorted(expectsortL, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()))
		else:
			sorted(expectsortL, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()), reverse=True)
		
		if sortedL == expectsortL:
			return ' correctly sorted with ' + kargs['params.sort.direction']
		else:
			raise Exception('Not correctly sorted')

	def sort_Mail_By_Date(self, **kargs):
		#send to sort requets
		#kargs['sortby'] = 'date'
		response = self.list_mail(**kargs)
		#get timestamp
		sortedL = utils.getMailReceivedDateFromMsgListRes(response)
		#send list request
		expectsortL = copy.copy(sortedL)
		if kargs['params.sort.direction'] == 'ascending':
			sorted(expectsortL)
		else:
			sorted(expectsortL, reverse=True)
		
		if sortedL == expectsortL:
			return ' correctly sorted with ' + kargs['params.sort.direction']
		else:
			raise Exception('Not correctly sorted')

	def sort_Mail_By_From(self, **kargs):
		#send to sort requets
		#sort by email field(from michael)
		kargs['sortby'] = 'from'
		response = self.list_mail(**kargs)
		sortedL_email = utils.getMailFromAddrFromMsgListRes(response)
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

	def sort_mail_by_flagged(self, **kargs):
		#kargs['sortby'] = 'flagged'
		response = self.list_mail(**kargs)
		sortedL_flagged = utils.getMailFlaggedFromMsgListRes(response)
		#send list request
		expectsortL = []
		if kargs['params.sort.direction'] == 'ascending':
			expectsortL = sorted(sortedL_flagged)
		else:
			expectsortL = sorted(sortedL_flagged, reverse=True)
		if sortedL_flagged == expectsortL:
			return ' correctly sorted with ' + kargs['params.sort.direction']
		else:
			raise Exception('Not correctly sorted')
			
	def sort_mail_by_attachment(self, **kargs):
		kargs['sortby'] = 'attachment'
		response = self.list_mail(**kargs)
		sortedL_attached = utils.getMailXattachFromMsgListRes(response)
		print sortedL_attached
		#send list request
		expectsortL = []
		if kargs['sortorder'] == 'ASC':
			expectsortL = sorted(sortedL_attached, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()))
		else:
			expectsortL = sorted(sortedL_attached, cmp=lambda x,y: cmp(x.encode('UTF-8').lower(),y.encode('UTF-8').lower()), reverse=True)
		if sortedL_attached == expectsortL:
			return ' correctly sorted with ' + kargs['sortorder']
		else:
			raise Exception('Not correctly sorted')
	
	def mail_advanced_search(self, **kargs):
		expectedCnt = int(kargs['expectedCnt'])
		kargs.pop('expectedCnt')
		folder_list = []
		if kargs.has_key('params.folderPaths'):
			folder_list = kargs['params.folderPaths']
		searchResp = self.advanced_search_mail(**kargs)
		msg_list = utils.getMailsByFolderFromSearchRes(folder_list, searchResp)
		if len(msg_list) == expectedCnt:
			pass
		else:
			raise Exception('%s mail expected, but %s returns.'%(expectedCnt, len(msg_list)))

	def check_read_receipt_msg(self,**kargs):
		expect_receipt_value = kargs['promptReturnReceipt'] == str(True)
		kargs.pop('promptReturnReceipt')
		msgFetchResp = self.msg_fetch(**kargs)
		receipt_value = utils.getReturnReceiptValsFromFetchRes(msgFetchResp)
		if receipt_value != expect_receipt_value:
			raise Exception('Expect value of returnReceipt is %s, but actuall it is %s'%(expect_receipt_value, receipt_value))

	def check_answered_flag_msg(self,**kargs):
		expect_value = kargs['answeredVal'] == str(True)
		mail_id = kargs['uid']
		kargs.pop('answeredVal')
		kargs.pop('uid')
		msgListResp = self.list_mail(**kargs)
		answered_value = utils.getAnsweredValByMailID(msgListResp, mail_id)
		if answered_value != expect_value:
			raise Exception('Expect value of answered flag is %s, but actuall it is %s'%(expect_value, answered_value))	

	def check_forwarded_flag_msg(self,**kargs):
		expect_value = kargs['forwardedVal'] == str(True)
		mail_id = kargs['uid']
		kargs.pop('forwardedVal')
		kargs.pop('uid')
		msgListResp = self.list_mail(**kargs)
		forwarded_value = utils.getForwardedValByMailID(msgListResp, mail_id)
		if forwarded_value != expect_value:
			raise Exception('Expect value of answered flag is %s, but actuall it is %s'%(expect_value, forwarded_value))	
			
	def block_senders(self, **kargs):
		'''
		domain=${common_domain}	n=250
		'''
		blocked = 'contact'
		for i in range(int(kargs['n'])):
			h={'sender':blocked+str(i+301)+kargs['domain']}
			self.block_sender(**h)
		return 'set ' + kargs['n']

	def change_pwd_positive(self, **kargs):
		response = self.change_pwd(**kargs)
		'''
		if 'ok' in response:
			return 'password changed.'
		else:
			raise Exception('change password failed!')	
		'''

	def get_external_account_id(self, **kargs):
		accountListResp = self.list_external_account()
		ids = utils.getExternalAccIDByUserName(kargs['username'], accountListResp)
		if len(ids) == 0:
			raise Exception('Can not find external account with name %s !'%kargs['username'])
		return ids[0]

	def get_date_from_msg_header_list(self, **kargs):
		'''
		input: 
			fieldname : the date field you want to check 
			subject: the mail subject
		description:
			get the date value
		'''
		subject = kargs['subject']
		kargs.pop('subject')
		field_name = kargs['fieldName']
		kargs.pop('fieldName')
		resp = self.list_mail(**kargs)
		time_value_list = utils.getDateValueBySubjectAndFieldName(resp,  field_name, subject)
		target_time = time_value_list[0]
		return target_time

	def get_date_from_msg_fetch(self, **kargs):
		'''
		input: 
			fieldname : the date field you want to check 
			subject: the mail subject
			mail id : for fetch request
			mail folder : for fetch request
		description:
			get the date value
		'''
		field_name = kargs['fieldName']
		kargs.pop('fieldName')
		subject = kargs['subject']
		kargs.pop('subject')
		fetch_response = self.msg_fetch(**kargs)
		time_value_list = utils.getDateValueFromFetchRes(fetch_response,  field_name, subject)
		target_time = time_value_list[0]
		return target_time

	def get_date_from_vmsgheaderlist(self, **kargs):
		field_name = kargs['fieldName']
		kargs.pop('fieldName')
		subject = kargs['params.subject']
		searchResp = self.advanced_search_mail(**kargs)
		time_value_list = utils.getDateValueBySubjectAndFieldName(searchResp, field_name, subject)
		target_time = time_value_list[0]
		return target_time
		
	def get_date_from_savemsgres(self, **kargs):
		saveMsgResp = self.save_draft(**kargs)
		time_value_list = utils.getDateValueBySubjectAndFieldName(saveMsgResp,  kargs['fieldName'], kargs['subject'])
		target_time = time_value_list[0]
		return target_time
		
	def __is_timezone_format_correct(self, original_str, original_fmt, original_timezone):
		'''
		input:
			
		output:
			true : timezone setting correctly
			false : timezone works incorrectly
			
		description:
			check if the server format time correctly be timezone by comparing it with local formating.
		'''
		sys_delta = 5 #minutes - diff of server and local machne, and method exec time

		import time, datetime, pytz
		#local timestamp
		local_timestamp = time.time()
		print 'local timestamp is : %s'%local_timestamp
		
		#fusion timestamp
		timeStamp_target = original_str/1000
		print 'fusion timestamp is : %s'%timeStamp_target
		
		#get time delta
		#delta_seconds = (localtime - targettime).seconds
		delta_seconds = abs(local_timestamp - timeStamp_target)
		print 'delta seconds is : %s'%delta_seconds
		#check if delta is OK
		if delta_seconds < sys_delta*60 :
			return True
		else:
			return False	

	# def __is_timezone_format_correct(self, original_str, original_fmt, original_timezone):
		# '''
		# input:
			# original_str : 20140930T143658
			# original_fmt : %Y%m%dT%H%M%S
			# timezone : original used timezone 
			
		# output:
			# true : timezone setting correctly
			# false : timezone works incorrectly
			
		# description:
			# check if the server format time correctly be timezone by comparing it with local formating.
		# '''
		# sys_delta = 5 #minutes - diff of server and local machne, and method exec time
		# import time, datetime, pytz
		# #local time - format with target timezone
		# tz = pytz.timezone(original_timezone)
		# localt = datetime.datetime.now(tz)
		# str_localtime = localt.strftime(original_fmt)
		# localtime = datetime.datetime.strptime(str_localtime, original_fmt)
		# #localtime = localtime.replace(tzinfo=None)
		# print 'correct time is : %s (please double check!)'%localtime
		# timeStamp_local = int(time.mktime(localtime.timetuple()))
		# print 'correct timestamp is : %s'%timeStamp_local
		# #target time - format by kiwi-octane
		# targettime = datetime.datetime.strptime(original_str, original_fmt)
		# print 'fusion time is : %s'%targettime
		# timeStamp_target = int(time.mktime(targettime.timetuple()))
		# print 'fusion timestamp is : %s'%timeStamp_target
		
		# #get time delta
		# #delta_seconds = (localtime - targettime).seconds
		# delta_seconds = abs(timeStamp_local - original_str/1000)
		# print 'delta seconds is : %s'%delta_seconds
		# #check if delta is OK
		# if delta_seconds < sys_delta*60 :
			# return True
		# else:
			# return False
			
	def check_tz_format(self, **kargs):
		'''
		input:
			targetdate : date used for time checking, original format is : 20140930T143658
		'''
		result = self.__is_timezone_format_correct(kargs['targetdate'], kargs['format'], kargs['timezone'])
		if result:
			print 'timezone(%s) setting works correctly.'%kargs['timezone']
		else:
			raise Exception('timezone(%s) setting works incorrectly!!!'%kargs['timezone'])

	#not used
	def get_timezone_for_test(self, **kargs):
		tz_res = self.list_timezone(**kargs)
		id_list = utils.getTimezoneIDList(tz_res)
		return id_list
		
	def get_timezone_by_gmt(self, **kargs):
		gmt_list = kargs['gmt']
		kargs.pop('gmt')
		tz_res = self.list_timezone(**kargs)
		timezone_map = utils.getTimezoneMap(tz_res)
		result_tz = []
		for gmt in timezone_map.keys():
			if gmt in gmt_list:
				result_tz = result_tz + timezone_map[gmt]
		return result_tz

	def check_send_max_mail(self, **kargs):
		#max_size = int(kargs['maxSendSize'])
		#kargs.pop('maxSendSize')
		try:
			res = self.send_mail(**kargs)
		except Exception, e:
			if msgconsts.MSG_TOO_LARGE in str(e):
				return
		raise Exception('Should raise mail too larg exception, but actually not!')
		
	def check_get_quota(self, **kargs):
		res = self.get_quota(**kargs)
		if res == 'null':
			raise Exception('No quota info found!')
		result_obj = json.loads(res)
		limit_value = result_obj['usedBytes']
		usage_value = result_obj['limitBytes']
		try:
			limit = int(limit_value)
			usage = int(usage_value)
		except Exception,e:
			raise Exception('Get quota failed! limit:%s, usage:%s. %s'%(limit_value, usage_value, str(e)))

	def check_mobile_signature(self, **kargs):
		expectStr = kargs['expectStr']
		kargs.pop('expectStr')
		res = self.load_mobile_signature(**kargs)
		if expectStr not in res:
			raise Exception('Expect str(%s) not in res(%s)'%(expectStr, res))
	
	def check_get_autoreply(self, **kargs):
		try:
			expectionStr = utils.getAutoReplyExpection(kargs['name'],kargs['value'])
			check_result = utils.checkStrFromResp(expectionStr,kargs['res'])
			return '%s with %s is checked'%(kargs['name'],kargs['value'])
		except Exception,e:
			raise Exception(e)
			
	def get_date_from_response(self,**kargs):
		try:
			date = utils.getDate(kargs['date'],kargs['response'])
			print '%s is got: %s'%(kargs['date'], date)
			return date
		except Exception,e:
			raise Exception(e)
	
	def create_attachments_params(self,**kargs):
		return kargs

	def empty_trustsenders(self,**kargs):
		try:
			res = self.list_trust_sender()
			sender_list = json.loads(res)
			if [] == sender_list:
				return
			else:
				sender_ids = []
				for sender in sender_list:
					sender_ids.append(sender['id'])
				print sender_ids
				kargs['params.ids'] = sender_ids
				res = self.delete_trust_sender(**kargs)
		except:
			raise Exception('Failed to remove trustsender(s)')
	
	def check_trustsender_existed(self,**kargs):
		res = self.list_trust_sender()
		expectStr = kargs['expectStr']
		for str in expectStr.split(','):
			if not str in res:
				raise Exception('Can not find %s in %s!'%(str, res))

	def get_trustsender_id_by_address(self,**kargs):
		try:
			res = self.list_trust_sender()
			sender_list = json.loads(res)
			if [] == sender_list:
				raise Exception('No trust sender !')
			else:
				for sender in sender_list:
					if sender['address'] == kargs['address']:
						return sender['id']
		except Exception, e:
			raise e
		raise Exception('Can not find trust sender with address %s'%kargs['address'])
	
	def send_loop_requests(self, **kargs):
		n = int(kargs['n'])
		request_name = kargs['keyword']
		del kargs['n'], kargs['keyword']
		for i in range(n):
			exec 'self.%s(**kargs)'%request_name
		
		
		
	
	
if __name__=='__main__':
	print 'mail lib name space'
	#print user_login(username='username',password='password')