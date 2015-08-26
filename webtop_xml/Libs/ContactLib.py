import time, datetime, os, random, re, copy
import requests, urllib
import CommonLib, Upload,WebtopResponseWrap,RequestLib

class ContactLib:

	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)
		self.createdContactIds = []

	def create_addressbook(self, **kargs):
		self.useraddress = CommonLib.CommonLib.useraddress
		# self.dom = self.useraddress.split('@')[1]
		# self.name = self.useraddress.split('@')[0]
		PABName = 'PAB' +str(random.randint(1,1000))
		request = RequestLib.createAddressBook%PABName
		if kargs.has_key('specialDataName'):
			return request
		response = self.common.request_send(request)
		if 'name="%s"'%PABName in response:
			# self.pabId = re.findall('.*id="(PAB://.*/main--.*)" name=.*',response.replace('><','>\n<'))
			self.pabId = re.findall('.*id="(.*)" name=.*',response.replace('><','>\n<'))
			print 'created PabId is '+ str(self.pabId)
			return 'PAB created: '+PABName
		else:
			raise Exception()
		
	def list_addressbook(self):
		self.listPABResp = self.common.request_send(RequestLib.listAddressBookRequest)
		self.pabIds = re.findall('.*<addressbook id="(.*)" name=.*',self.listPABResp.replace('><','>\n<'))
		return str(len(self.pabIds)) + ' address books found!'
		
	def use_addressbook(self,**kargs):
		'''kargs['defaultPAB'], kargs['userPAB']'''
		self.list_addressbook()
		self.pabId = re.findall('id="([^"]*)"',self.listPABResp)
		# if kargs.has_key('defaultPAB'):
			# self.pabId =re.findall('.*<addressbook id="(.*)" name=".*<property name="default".*',self.listPABResp)
		if kargs.has_key('userPAB'):
			# self.pabId = re.findall('.*id="(.*)" name=[^Default].* type=.*',self.listPABResp.replace('><','>\n<'))
			self.pabId.pop(0)
		return self.pabId[0]
		
	def delete_addressbook(self,**kargs):
		'''kargs['all'] -> delete all addressbooks'''
		# pabList = re.findall('.*id="(PAB://.*/.*/main--.*)" name=.*',self.listPABResp.replace('><','>\n<'))
		pabList = re.findall('.*id="(.*)" name=.*',self.listPABResp.replace('><','>\n<'))
		pabList.pop(0)
		failLog = ''
		for pab in pabList:
			response = self.common.request_send(RequestLib.deleteAddressBook%pab)
			if '<addressbooks action="delete" />' not in response:
				failLog = failLog + pab.split('main--')[1] + '\n'
			if not kargs.has_key('all'):
				if failLog:
					return failLog
				else:
					return 'Addressbook(s) deleted'
		if failLog:
			return failLog
		else:
			return 'Addressbook(s) deleted'		
		
	def create_contact_group(self,**kargs):
		self.useraddress = CommonLib.CommonLib.useraddress
		# self.dom = self.useraddress.split('@')[1]
		# self.name = self.useraddress.split('@')[0]
		
		groupName = 'group'+str(random.randint(1,1000))
		request = RequestLib.createGroup%(self.pabId[0], groupName)
		if kargs.has_key('specialDataName'):
			return request
		response = self.common.request_send(request)
		groupId = re.findall('.*<contactgroup id="(PAB://.*)" name=.*',response.replace('><','>\n<'))
		if groupId:
			return groupId[0]
		else:
			raise Exception('Failed to create contact group')
		
	def list_contact_group(self,**kargs):
		'''kargs['defaultPAB'], kargs['userPAB']'''
		self.use_addressbook(**kargs)
		response = self.common.request_send(RequestLib.listGroup%self.pabId[0])
		self.groupIds = re.findall('.*<contactgroup id="(PAB://.*GROUP_.*)" name=.*',response.replace('><','>\n<'))
		return str(len(self.groupIds)) + ' contact groups found!'
		
	def delete_contact_group(self,**kargs):
		'''	kargs['defaultPAB'] -> contact groups from default PAB
			kargs['userPAB'] -> contact groups from 1st user-created PAB
			kargs['all'] -> delete all addressbooks'''
		self.list_contact_group(**kargs)
		failLog = ''
		for id in self.groupIds:
			response = self.common.request_send(RequestLib.deleteGroup%(self.pabId[0],id))
			if '<contacts action="delete_group" />' not in response:
				failLog = failLog + id.split('main/')[1].split('"')[0]+'\n'
			if not kargs.has_key('all'):
				if failLog:
					return failLog
				else:
					return 'Contact group(s) deleted' 	
		if failLog:
			return failLog
		else:
			return 'Contact group(s) deleted'		
			
	def get_group(self,**kargs):
		'''	kargs['defaultPAB'] -> contact groups from default PAB
			kargs['userPAB'] -> contact groups from 1st user-created PAB'''
		self.list_contact_group(**kargs)
		response = self.common.request_send(RequestLib.getGroup%(self.pabId[0], self.groupIds[0]))
		getgroupResp = re.findall('<contacts action="get_group"><contactgroup id=".*" name=".*',response)
		if getgroupResp:
			return 'Get group!'
		else:
			raise Exception('Failed in get_group api')
	
	def list_contacts(self,**kargs):
		'''	kargs['defaultPAB'] -> contact groups from default PAB
			kargs['userPAB'] -> contact groups from 1st user-created PAB'''
		self.use_addressbook(**kargs)
		response = self.common.request_send(RequestLib.listContacts%self.pabId[0])
		if 'CONTACT_' in response:
			self.contactIds = re.findall('.*<contact id="(PAB://.*/CONTACT_.*)" firstName=".*', response.replace('><','>\n<'))
		else:
			self.contactIds = re.findall('.*<contact id="(.*)" firstName=".*', response.replace('><','>\n<'))
		self.fistConNode = '<contact '+response.split('<contact ')[1].split('</contact>')[0]+'</contact>'
		return str(len(self.contactIds)) + ' contacts found!'
		
	def create_basic_contact(self,**kargs):
		'''	need: firstName="%s" lastName="%s" name="%s"
			if needMoreInfo: set self.contactInfoWrap to be edited, else set request to be send '''
		kargs['id'] = kargs['addressBookId'] = self.pabId[0]
		if kargs.has_key('firstName'):
			self.originalFn = kargs['firstName']
		if kargs.has_key('lastName'):
			self.originalLn = kargs['lastName']
		
		originalReq = self.common.request_send(RequestLib.createContact,kargs,getRes=True)
		if kargs.has_key('needMoreInfo'):
			self.contactInfoWrap = WebtopResponseWrap.WebtopResponseWrap(originalReq)
			del kargs['needMoreInfo']
		else:
			self.createContactReq = originalReq
		
		del kargs['addressBookId']
		self.InputCI = [] # saved contact info from case attr for check contact in future
		self.InputCI.append(kargs)
		return 'Basic contact info is ' + originalReq
	
	def set_more_info(self,**kargs):
		'''	need: kargs['label'], kargs['type'], kargs['value'] -> usage example for case:
				<contactfield id="" contact_id="" label="middlename" type="lzHeader" value="mmm" primary="false"/>
				<contactfield id="" contact_id="" label="nickname" type="lzHeader" value="nnn" primary="false"/>
				<contactfield id="" contact_id="" label="work" type="lzEmail" value="2r2r@sdfw.com" primary="false"/>
				<contactfield id="" contact_id="" label="home" type="lzPhone_mobile" value="" primary="false"/>
				<contactfield id="" contact_id="" label="home" type="lzPhone" value="" primary="false"/>
				<contactfield id="" contact_id="" label="birthday" type="lzPersonal" value="20140605" primary="false"/>
				<contactfield id="" contact_id="" label="title" type="lzHeader" value="poooosition" primary="false"/>
				<contactfield id="" contact_id="" label="department" type="lzHeader" value="dddpartment" primary="false"/>
				<contactfield id="" contact_id="" label="company" type="lzHeader" value="ccccompany" primary="false"/>
				<contactfield id="" contact_id="" label="home" type="lzPhone_fax" value="123213" primary="false"/>
				<contactfield id="" contact_id="" label="home" type="lzPhone_pager" value="1323" primary="false"/>
				<contactfield id="" contact_id="" label="google" type="lzIM" value="sdf@gmail.com" primary="false"/>
				<contactfield id="" contact_id="" label="home" type="lzWeb" value="http://www.baidu.com" primary="false"/>
				<contactfield id="" contact_id="" label="notes" type="lzNote" value="blablabla" primary="false"/>
				<contactfield id="" contact_id="" label="sdf" type="lzOther" value="sdfsdfsdf" primary="false"/>
				<contactfield id="" contact_id="" label="street" type="lzAddress_home" value="sdf" primary="false"/>
				<contactfield id="" contact_id="" label="street2" type="lzAddress_home" value="asdf" primary="false"/>
				<contactfield id="" contact_id="" label="street3" type="lzAddress_home" value="asdf" primary="false"/>
				<contactfield id="" contact_id="" label="city" type="lzAddress_home" value="sdf" primary="false"/>
				<contactfield id="" contact_id="" label="state" type="lzAddress_home" value="sdf" primary="false"/>
				<contactfield id="" contact_id="" label="zip" type="lzAddress_home" value="sdfsd" primary="false"/>
				<contactfield id="" contact_id="" label="country" type="lzAddress_home" value="fds" primary="false"/>'''
		self.contactInfoWrap.addElement(xPath='contact', tag='contactfield', attrib=kargs, valueText='')
		self.InputCI.append(kargs) # saved contact info from case attr for check contact in future
		self.keyword = kargs
		return kargs
		
	def send_save_contact(self,**kargs):
		if kargs.has_key('withmoreInfo'):
			self.createContactReq = self.contactInfoWrap.toXML()
		if kargs.has_key('updatemoreInfo'):
			self.createContactReq = self.contactInfoWrap.toXML()
			self.createContactReq = self.createContactReq.replace('<contactfield','<contactfield id="" contact_id="%s"'%self.updateContactId)
		if kargs.has_key('specialDataName'):
			return self.createContactReq
			
		request = self.common.request_send(self.createContactReq)	
		if not kargs.has_key('updatemoreInfo'):
			cid = re.findall('.*contact id="(.*)" firstName=.*',request.replace('><','>\n<'))
			self.updateContactId = cid[0]
			if not cid:
				raise Exception('Failed to save a contact')
			else:
				self.createdContactIds.append(cid[0])
				print '-------------------------------- Contact saved --------------------------------\n'
				return str(cid[0])
		else:
			print '-------------------------------- Contact updated  --------------------------------\n'
			return self.updateContactId
		
	def delete_contacts(self,**kargs):
		'''	kargs['defaultPAB'] -> contact groups from default PAB
			kargs['userPAB'] -> contact groups from 1st user-created PAB
			kargs['fromGroup'] -> get the contact group if need to delete from group
			kargs['all'] -> delete all addressbooks'''
		self.list_contacts(**kargs)
		failLog = ''
		request = self.common.request_send(RequestLib.deleteContact%self.pabId[0],getRes=True)
		contactlistWrap = WebtopResponseWrap.WebtopResponseWrap(request)
		for id in self.contactIds: # add contact nodes into one request
			contactlistWrap.addElement(xPath='contacts', tag='contact', attrib={'id':id}, valueText='')
			if not kargs.has_key('all'):
				break
		if kargs.has_key('fromGroup'): # add groupId attribute into the request
			del kargs['fromGroup']
			self.list_contact_group(**kargs)
			contactlistWrap.setElementValue(xPath='contacts', valueText='', attrib={'group_id':self.groupIds[0]})
			
		response = self.common.request_send(contactlistWrap.toXML())
		if '<contacts action="delete_contact" />' in response:
			return str(len(re.findall('<contact id="PAB', contactlistWrap.toXML())))+' contact(s) deleted! '
		else:
			raise Exception('failed to delete contact(s)! ')+str(len(re.findall('<contact id="PAB', contactlistWrap.toXML())))
			
	def move_between_pab_group(self, **kargs):
		'''	assign a contact from pab to group, default is assign, if kargs['remove'] -> remove from group to PAB
			kargs['defaultPAB'] -> assign/remove contact to default PAB
			kargs['userPAB'] -> assign/remove contact to user-created PAB
			kargs['all'] -> assign/remove all addressbooks'''
		self.list_contact_group(**kargs)
		self.list_contacts(**kargs)
		request = RequestLib.addGroupContact%(self.pabId[0], self.groupIds[0])
		expect = '<contacts action="add_group_contact" />'
		if kargs.has_key('remove'):
			request = request.replace('add_group_contact', 'delete_group_contact')
			expect = '<contacts action="delete_group_contact" />'
			del kargs['remove']
		pabGroupWrap = WebtopResponseWrap.WebtopResponseWrap(request)
		for id in self.contactIds: # add contact nodes into one request
			pabGroupWrap.addElement(xPath='contacts', tag='contact', attrib={'id':id}, valueText='')
			if not kargs.has_key('all'):
				break
		
		response = self.common.request_send(pabGroupWrap.toXML())		
		if expect in response:
			return str(len(re.findall('<contact id="PAB', pabGroupWrap.toXML())))+' contact(s) moved with ' + expect
		else:
			raise Exception('Failed to moved contact(s) with ' + expect)
		
	def search_sort_contact(self, **kargs):
		'''	Both kargs are optional:
			kargs['keywords'] -> keywords for search
			kargs['sort'] -> 'firstName ASC', 'firstName DESC', 'lastName ASC', 'lastName DESC', 'email ASC', 'email DESC' '''
		log = ''
		if kargs.has_key('keywords'):
			kargs['filter'] = kargs['keywords']
			del kargs['keywords']
			log = log + '[SEARCH]'
		if kargs.has_key('sort'):
			sortField = kargs['sort'].split()[0]
			order = kargs['sort'].split()[1]
			log = log + '[SORT]'

		request = RequestLib.listContacts%self.pabId[0]
		listWrap = WebtopResponseWrap.WebtopResponseWrap(request)
		listWrap.setElementValue(xPath='contacts', valueText='', attrib = kargs, index=0)
		response = self.common.request_send(listWrap.toXML())
		
		contactsL = re.findall('.*(.*CONTACT_.*).*',response.replace('><','>\n<'))
		if 'SEARCH' in log:
			log = log + str(len(contactsL))+'\n'
		if 'SORT' in log:
			sortedL = re.findall('.*contact id="PAB://.*%s="(.*)".*modifiedTime="0">.*'%sortField,response.replace('><','>\n<'))
			contactsL = re.findall('.*contact id="PAB://.*(CONTACT_.*%s=".*)".*modifiedTime="0">.*'%sortField,response.replace('><','>\n<'))
			
			sortedContacts = ''
			for contact in contactsL:
				sortedContacts = sortedContacts + contact + '\n'
			print str(len(contactsL))+' get sorted:\n'+sortedContacts
			
			expectsortL = copy.copy(sortedL)
			if order == 'ASC':
				expectsortL.sort()
			else:
				expectsortL.sort()
				expectsortL.reverse()
			if sortedL == expectsortL:
				log = log + ' correctly sorted with '+order
			else:
				raise Exception('Not correctly sorted')
		return log		
			
	def list_contact_dup(self, **kargs):
		''' Include use_addressbook:
			kargs['defaultPAB'] -> contact groups from default PAB
			kargs['userPAB'] -> contact groups from 1st user-created PAB
			Output: self.duplist-> dup contact ids, self.contactIdXML -> piece contact ids to xml nodes'''
		self.use_addressbook(**kargs)
		response = self.common.request_send(RequestLib.listdup%self.pabId[0])
		firstGroupResp = response.split('</dupe>')[0]
		self.duplist = re.findall('.*<contact id="(.*)" />.*',firstGroupResp.replace('><','>\n<'))
		self.contactIdXML = ''
		for contact in self.duplist:
			self.contactIdXML = self.contactIdXML + '<contact id="%s"/>'%contact
		return str(len(self.duplist)) + ' dup find, the first one is ' + self.duplist[0]
		
	def get_contacts_merge(self,**kargs):
		'''	This function is for merge contacts
			kargs['fromDup'] -> used list_contact_dup before, else -> works directly to merge newly created contacts '''
		if not kargs.has_key('fromDup'): # define dup ids and piece to the xml, define for new merge contact
			self.contactIdXML = ''
			for contact in self.createdContactIds:
				self.contactIdXML = self.contactIdXML + '<contact id="%s"/>'%contact
			self.updateContactId = self.createdContactIds.pop(0)
			self.deleteContactIds = self.createdContactIds
		else:
			self.updateContactId = self.duplist.pop(0) 
			self.deleteContactIds = self.duplist
			
		request = RequestLib.getContactsInfo.split('</contacts>')[0]+ self.contactIdXML + '</contacts>'+RequestLib.getContactsInfo.split('</contacts>')[1]
		response = self.common.request_send(request%self.pabId[0])
		
		# expect =  self._getContactsInfo(response)
		self._preview_mergeUpdate()
		self._deleteDups()
		return 'Contacts Previewed, Merged and Updated! Dup contacts deleted'
		
	def check_contact(self, **kargs):
		request = RequestLib.getContactsInfo.split('</contacts>')[0]+ '<contact id="%s"/>'%kargs['id'] + '</contacts>'+RequestLib.getContactsInfo.split('</contacts>')[1]
		response = self.common.request_send(request%self.pabId[0])
		self._getContactsInfo(response)
		failedLog = ''
		for contact in self.contactList:
			if kargs['id'] in contact:
				for expectH in self.InputCI:
					for expectItem in expectH:
						if '%s=%s'%(expectItem, expectH[expectItem]) in contact:
							pass
						else:
							failedLog = failedLog + '%s=%s'%(expectItem, expectH[expectItem]) + '\n'		
			else:
				pass
		if failedLog:
			raise Exception('Not found '+failedLog)
		else:
			print 'Checked '+str(self.InputCI) +' in '+str(self.contactList)
			return 'Checked!'
			
	def _getContactsInfo(self,getContactResp):
		
		contactlistXML = getContactResp.split('<contacts action="get_contacts">')[1].split('</contacts>')[0]
		infoXMLlist = contactlistXML.split('</contact>')
		self.contactList = [] # save all dup contacts as list of hashes
		i = 0
		infoXMLlist.pop(-1)
		for infoXML in infoXMLlist: # infoXML -> each piece of contact xml
			infoHash = {} # infoHash -> each contact info save in one hash
			infoHash['index']=i
			i+=1
			lines = re.findall( '.*(<.*)>.*',infoXML.replace('><','>\n<'))  # <contactfield label="home" type="lzEmail" value="vvnmay@opal.qa.laszlosystems.com" primary="false" />
			self.contactList.append(lines)
		
	def _preview_mergeUpdate(self):
		previewResp = self.common.request_send(RequestLib.previewMerge%(self.pabId[0], self.contactIdXML))
		if '<contacts action="preview_merge">' in previewResp:
			print 'Contacts previewd with response:\n'+previewResp
		else:
			raise Exception('Failed to preview merge info.')
		contactNodesXML = previewResp.split('<contacts action="preview_merge">')[1].split('</contact>')[0]
		# for update
		# # <response tokenExpiry="86395699" sessionId="dR__HeZY-41" token="b4c7889e99d03172aadebf4b779bfcaad958946f0f852c7fe2e4b00f3fd22eed811781113f913192cb9eae2884847fcff2a3592b32da4d01c0e7b67372c5a619da977bb2f379cf703d156aabf23c49fc">
		# # <contacts action="preview_merge">
		# OUTPUT -> contactNodesXML
		# # <contact firstName="fname" lastName="" modifiedTime="0">
		# <contactfield label="home" type="lzEmail" value="vvnmay1@opal.qa.laszlosystems.com" primary="false" />
		# <contactfield label="work" type="lzEmail" value="vvnmay1@opal.qa.laszlosystems.com" primary="false" />
		# <contactfield label="home" type="lzPhone_mobile" value="234" primary="false" />
		# <contactfield label="available" type="lzPhoto" value="false" primary="false" />
		# <contactfield label="home" type="lzEmail" value="" primary="true" />
		# 
		# </contact>
		# # </contacts>
		# # </response>		
		contactAttr = {'contactXML':contactNodesXML}
		self.update_contact(**contactAttr)
		
	def update_contact(self,**kargs):
		if kargs.has_key('contactXML'): # for preview update
			contactXML = kargs['contactXML']
			newFirstName = contactXML.split('firstName="')[1].split('"')[0]
			newLastName = contactXML.split('lastName="')[1].split('"')[0]
			fieldXML = contactXML.replace(contactXML.split('<contactfield')[0],'')
			contactXML = fieldXML.replace('<contactfield','<contactfield id="" contact_id="%s"'%self.updateContactId)	

		else: # for just created
			newFirstName = self.originalFn + '_updated'
			newLastName = self.originalLn + '_updated'
			contactIdXML = '<contact id="%s"/>'%self.updateContactId
			request = RequestLib.getContactsInfo.split('</contacts>')[0]+ contactIdXML + '</contacts>'+RequestLib.getContactsInfo.split('</contacts>')[1]
			request = request%self.pabId[0]
			response = self.common.request_send(request)
			contactXML = response.replace('</contact></contacts></response>','')
			
			contactXML = contactXML.replace(contactXML.split('<contactfield')[0],'')
		# contactXML = fieldXML.replace('<contactfield','<contactfield id="" contact_id="%s"'%self.updateContactId)	
		
		
		# new name from test case kargs	
		if kargs.has_key('newFirstName'):
			newFirstName = kargs['newFirstName']
		if kargs.has_key('newLastName'):
			newLastName = kargs['newLastName']	
			
		updateReq = RequestLib.updateContact%(self.pabId[0], self.updateContactId, newFirstName, newLastName,'')
		updateReq = updateReq .replace('fieldbody', contactXML)
		
		if kargs.has_key('needMoreInfo'):
			self.contactInfoWrap = WebtopResponseWrap.WebtopResponseWrap(updateReq)
		else:
			self.createContactReq = updateReq
		return 'Basic contact info is ' + updateReq
		
		response = self.common.request_send(updateReq) # not need more info, update directly
		if '<contacts action="update_contact" />' in response:
			print 'Contacts updated, name is %s %s '%(newFirstName, newLastName)
		else:
			raise Exception('Failed to update contacts')
			
	def _deleteDups(self):
		deleteContactsXML = ''
		for deleteid in self.deleteContactIds:
			deleteContactsXML = deleteContactsXML + '<contact id="%s"/>'%deleteid
		deleteReq = RequestLib.deleteContact%self.pabId[0]
		deleteReq = deleteReq.replace('</contacts>', deleteContactsXML+'</contacts>')
		response = self.common.request_send(deleteReq)
		if '<contacts action="delete_contact" />' in response:
			print 'Dup contcts deleted: %d contacts'%len(self.deleteContactIds)
		else:
			raise Exception('Failed to delete dup contacts')
		
	def set_autosuggest_onoff(self,**kargs):
		'''	This is autosuggestion setting
			kargs['on'] -> set autosuggest to on.
			if not has kargs['on'], set autosuggest to off'''
		value = False
		if kargs.has_key('on'):
			value = True
		self.common.request_send(RequestLib.autoSuggestCL%value)
		
		response = self.common.request_send('<request><prefs action="get" limit="25"></prefs></request>')
		if '<pref name="contacts.autoSuggestCL">%s</pref>'%str(value).capitalize() in response:
			return 'autosuggest is set to '+str(value)
		else:
			raise Exception('autosuggest is failed to set to '+str(value))
		
	def create_autocomplete(self, **kargs):
		# self.addr = self.address = kargs['address']
		# if kargs.has_key('name'):
			# self.address = '&quot;%s&quot; &lt;%s&gt;'%(kargs['name'], self.address)
		# response = self.common.request_send(RequestLib.createAutocompleteCont%self.address)
		# if self.address in response and re.findall('.*address="(.*)".*', response.replace('><','>\n<')):
			# self.autoCId = re.findall('.*address="(.*)".*', response.replace('><','>\n<'))[0]
			# print '%s is created as auto-complete contact'%self.addr
			# return self.autoCId
		# else:
			# raise Exception('%s is failed to be created as auto-complete contact'%self.addr)
		self.addr = kargs['address']
		response = self.common.request_send(RequestLib.createAutocompleteCont%self.addr)
		return 'Auto-complete contact created!'
		
	def go_suggest_and_check(self,**kargs):
		'''	kargs['kw'] -> keyword for auto-suggestion
			kargs['check'] -> if check is true, check the latest created auto-suggest contact xml list'''
		response = self.common.request_send(RequestLib.suggestRequest%kargs['kw'])
		if '<matches complete="true">' in response:
			pass
		else:
			raise Exception('No contact filtered out for suggestion!')
		if not kargs.has_key('check'):
			filtered = re.findall('contactfield label', response)
			self.suggestNumber = len(filtered)
			return 'Suggest: '+str(filtered)
		else: 
			if self.addr in response:
				return 'Created auto-suggest contact can be filtered with %s, %s'%(kargs['kw'], self.addr)
			else:
				raise Exception('Created auto-suggest contact canNOT be filtered with %s, %s'%(kargs['kw'], self.addr))
		
	def check_suggest_duplication(self, **kargs):
		if str(self.suggestNumber) == kargs['suggestNumber']:
			return 'Auto-complete contact suggestion duplication checked.'
		else:
			raise Exception('Auto-suggest conatcts number wrong, exist duplication.')
		
	def list_autocomplete(self):
		response = self.common.request_send(RequestLib.listAutocomplete)
		# if 'autocomplete id' in response and re.findall('.*<autocomplete .*address="(.*)" />.*', response.replace('><','>\n<')):
		if 'autocomplete id' in response and re.findall('.*<autocomplete id="(.*)" address=.*', response.replace('><','>\n<')):
			self.contactsTL = re.findall('.*<autocomplete id="(.*)" address=.*', response.replace('><','>\n<'))
			print self.contactsTL
		else:
			self.contactsTL = ''
		return self.contactsTL
		
	def delete_autocomplete(self,**kargs):
		'''	Need to run list_autocomplete first
			kargs['all'] -> delete all auto-complete contacts'''
		deleteXML = ''
		for addr in self.contactsTL:
			deleteXML = deleteXML + '<id>%s</id>'%addr
			if not kargs.has_key('all'):
				print 'not all, delete one'
				break
		
		response = self.common.request_send(RequestLib.deleteAutocomplete%deleteXML)
		if '<autocomplete action="delete" />' in response:
			return 'autocomplete contact(s) deleted'
		else:
			raise Exception('autocomplete contact(s) failed to be deleted')
		
	def export_contact(self,**kargs):
		'''	.vcf -> (UI) VCARD
			.csv -> (UI) CSV	'''
		url = kargs['url']+kargs['dlname']
		if kargs['dlname'].split('.')[1] == 'vcf':
			format = 'vcard3'
		elif kargs['dlname'].split('.')[1] == 'csv':
			format = 'outlook2010'
		else:
			raise Exception('download name should be ended with .vcf or .csv')
		
		data = {}
		rangeh = {'range':self.pabId[0]+'/cnt/CONTACT_23'}
		range = urllib.urlencode(rangeh).split('=')[1]
		data['r']='<resource resolver="contact" addressBookId="%s" format="%s" range="%s" />'%(self.pabId[0], format, range)
		data['addressBookId'] = self.pabId[0]
		r = self.common.session.post(url,data)
		if 'error code' in r.text:
			raise Exception('response error code: '+r.text.split('<error code="')[1].split('"')[0])   # eg. <error code="QUOTA_EXCEEDED">
		else:
			return 'Contact format [%s] has been exported as [%s] file'%(format, kargs['dlname'].split('.')[1])

	def import_contact(self,**kargs):
		fid = kargs['fid']
		resp = self.common.request_send(RequestLib.importContact%(self.pabId[0], fid))
		if '<contacts action="import">' in resp:
			return 'Contact is imported from attached file'
		else:
			raise Exception('Contact is failed to be imported from attached file')
		
	def send_vcard(self,**kargs):
		smartNode = '<smartobjects>' + self.fistConNode + '</smartobjects>'
		sendMailReq = self.common.request_send(RequestLib.msgsendRequest,kargs,getRes=True)
		request = sendMailReq.replace('</mail>',smartNode+'</mail>')
		resp = self.common.request_send(request)
		if '<status>ok</status>' in resp and '<mail action="msgsend">' in resp:
			return self.fistConNode
		else:
			raise Exception('Faied to send mail with vCard')

	def delete_all_AutoCMPLTContact(self, **kargs):
		try:
			self.list_autocomplete()
		except:
			pass

		if self.contactsTL:
			kargs['all'] = True
			self.delete_autocomplete(**kargs)
			
	def create_Max_AutoCMPLTContact(self, **kargs):
		kargs['maxCnt'] = '300'
		if not kargs['maxCnt']:
			raise Exception('not maxCount parameter found!')
		if kargs['maxCnt'] <= 0:
			raise Exception('input parameter maxCount is invalid!')
		maxCount = int(kargs['maxCnt']) + 2#one for range,one for more than max count
		for i in range(1,maxCount):
			try:
				kargs['name'] = 'name' + str(i)
				kargs['address'] = str(i) + 'name@test.com'
				res = self.create_autocomplete(**kargs)
			except Exception,e:
				if i == (maxCount - 1):#need to assert the error code
					return 'Can not create the %s autocompletecontace, the max count is %s'%(i, kargs['maxCnt'])
				else:
					raise e
		raise Exception("Max auto complete contact Count config doesn't work!")	

	def check_contact_count(self, **kargs):
		if kargs.has_key('expcount'):
			count = kargs['expcount']
			contactL = self.list_autocomplete()
			if int(count) == len(contactL):
				return 'the count of contact is %s, case pass.'%len(contactL)
			else:
				raise Exception(('expected count is %s, but the actual count is %s')%(count, str(len(contactL))))
		raise Exception('Invalid Parameter!')
	
		
	def check_AutoCMPLTContact_Filter(self, **kargs):
		#get filter
		expectCnt = int(kargs['expectCnt'])
		expectFldList = []
		if kargs.has_key('expectFld'):
			expectFldList = kargs['expectFld'].split(',')
		filterStr = kargs['filter']
		response = self.common.request_send(RequestLib.suggestRequest%filterStr)
		print response
		matchList = re.findall('<contact ', response.replace('><','>\n<'))
		if len(matchList) != expectCnt:
			raise Exception('[filter: %s]Expected to match %s contact, but %s contact returned!'%(filterStr, expectCnt, len(matchList)))
		if expectCnt == 0:
			return
		for expectFld in expectFldList:
			if not re.findall(expectFld, response.replace('><','>\n<')):
				raise Exception('[filter: %s]Did not match the expected contact!'%filterStr)

	def check_contact_dup(self, **kargs):
		exptDupCnt = int(kargs['exptDupCnt'])
		if int(exptDupCnt) > 0:
			exptDupContactCntL = kargs['exptDupContactCnt'].split(',')
		self.use_addressbook(**kargs)
		response = self.common.request_send(RequestLib.listdup%self.pabId[0])
		groupResp = response.split('</dupe>')[:-1]
		if len(groupResp) != exptDupCnt:
			raise Exception('Expected dup count is %s, but returned dup count is %s'%(exptDupCnt, len(groupResp)))
		if exptDupCnt == 0:
			return			
		for (resp,contactcnt) in zip(groupResp, exptDupContactCntL):
			duplist = re.findall('.*<contact id="(PAB://.*CONTACT_.*)" />.*', resp.replace('><','>\n<'))
			if len(duplist) != int(contactcnt):
				raise Exception('Expected contact count is %s, but returned contact count is %s'%(contactcnt, len(duplist)))
			
				
	# ---------feature will be removed for sbm-----------
	def set_photo(self, uploadURL, filePath):
		photo = Upload.uploadResource(uploadURL, filePath, "2014-06-05", "myFileName")
		print photo["id"] + " : " + photo["filename"]
		
		
# newfile = open('E:\\Repositaries\\robot\\workspace\\Libs\\tmp.txt','w')
# newfile.write(res.read()) # str(re.findall('.*(<todo summary.*/todo>).*',TaskResp))
# newfile.close()