import time, datetime, os, random, re, copy, sys, urllib, Upload
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder, TestCodeException, msgconsts
from Contact import Contact
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
import MailLib

class ContactLib(Contact):

	def __init__(self,url):
		Contact.__init__(self, url)
		self.url = url
		self.mail = MailLib.MailLib(url)
	
	#-----function for test check-------------------------------------
	def get_all_idList_by_last_id(self, **kargs):
		last_id = kargs['lastId']
		if type(last_id) == list:
			last_id = kargs['lastId'][-1]
		last_id = kargs['lastId'].encode('utf-8')
		id_url = last_id.split('_')[:-1][0] # like PAB://openwave.com/webtop8/main/grp/GROUP
		last_num = int(last_id.split('_')[-1]) # like 87
		idList = []
		for i in range(last_num):
			idList.append(id_url +'_' + str(i+1))
		print 'there are %d ids'%len(idList)
		return idList
				
	def check_created_id_by_name(self, **kargs):
		'''
		input : name - contact group name
				addressbook_id
				expectCnt - expect number of addressbook
		description : check if the contact group is right
		
		'''
		result_id = utils.getCreatedIdFromRes(**kargs)
		return result_id
	
	def get_addressbook_id_by_name(self, **kargs): # = self.list_addressbook() + check_created_id_by_name()
		'''kargs['name'] - addressbook name: Defualt or user created addressbook name'''
		kargs['res'] = self.list_addressbook()
		return self.check_created_id_by_name(**kargs)
				
	def check_contact_in_group_by_name(self, **kargs):
		'''
		input : params.addressBookId
				params.groupId
				contactL - expected contacts (a list)
				expectCnt - expect number of addressbook
		description : check if the contact in certain group is right
		note - getContactsL =
					[ 	{
						  "@type" : "Contact",
						  "id" : "PAB://openwave.com/webtop8/main/cnt/CONTACT_67",
						  "firstName" : "testFirst1",
						  "lastName" : "testLast",
						  "email" : "",
						  "fields" : 
						  [ {
							"label" : "available",
							"type" : "lzPhoto",
							"value" : "false"
						  } ],
						  "modifiedTime" : 0
						} 	] 	'''
		getgroupKargs = {'params.addressBookId':kargs['params.addressBookId'], 'params.groupId':kargs['params.groupId']}
		result = self.get_group(**getgroupKargs)# use get group request !
		getContactsL = eval(result)['contacts']
		foundL = []
		for expect_contact in kargs['contactL']:
			for contact in getContactsL:
				if contact['id'] == expect_contact:
					foundL.append(expect_contact.encode('utf-8'))
		
		if kargs.has_key('expectCnt'):
			expectCnt = int(kargs['expectCnt'])
			if len(foundL) != expectCnt:
				raise Exception('Expect count of contact is %s, but actually got %s'%(expectCnt, len(foundL)))	
		
	def check_list_contact_afterMerge_byPreview(self, **kargs):
		'''	mergePreview=${merge_preview result}
			listMerge=${list after merged result}'''
		mergePreview = eval(kargs['mergePreview'].replace('null','\"\"'))
		mergePreview.pop('id')
		list_results = eval(kargs['listMerge'])['results']
		merged_result = list_results[0]
		merged_result.pop('id')
		merged_result.pop('addressBookId') # merge preview doesnot have addressBookId
		failed = ''
		for item in merged_result:
			if item == 'fields':
				if merged_result[item][0]==mergePreview[item][0]:
					pass
			elif merged_result[item] == mergePreview[item]:
					pass
			else:
				failed = failed + '[%s]merge preview is %s but list merged_result is %s'%(item, mergePreview[item], merged_result[item])
		if failed:
			raise Exception(failed)
		return 'All contact info checked for merged contact by merge preview'
		
	def empty_addressbook(self, **kargs):
		res = eval(self.list_addressbook())
		if len(res) == 1:
			return 'Only left a default addressbook'
		id_list = []
		for addr in res:
			if not addr['id'].split('/')[-1] == 'main':
				kargs['params.ids'] = addr['id']
				self.del_addressbook(**kargs)
				del kargs['params.ids']
			
	def makeContactField(self, **kargs):
		for i in kargs:
			if type(kargs[i]) == unicode:
				kargs[i]=kargs[i].encode('utf-8')
		return kargs
		
	def make_contact(self, **kargs):
		for i in kargs:
			if type(kargs[i]) == unicode:
				kargs[i]=kargs[i].encode('utf-8')
		print kargs
		return kargs
		
	def list_sort_condition(self, **kargs):
		'''	kargs : lastName=ascending	firstName=ascending
			return : [ {"field":"lastName","direction":"ascending"}, {"field":"firstName","direction":"ascending"}]
		'''
		list=[]
		for key in kargs:
			field_direction = {'field': key.encode('utf-8'), 'direction':kargs[key].encode('utf-8')}
			list.append(field_direction)
		return list
			
	def check_order(self, **kargs):
		results_list = eval(kargs['res'])['results']
		orderBy = kargs['order'].split(' ')[0] # samefirst lastName
		order = kargs['order'].split(' ')[1] # ASC DESC
		
		order_list = []
		for contact in results_list:
			order_list.append(contact[orderBy])
		expectOrder = copy.copy(order_list)
		
		if order == 'ASC':
			expectOrder.sort()
		else:			
			expectOrder.sort(reverse=True)
			
		if 	order_list == expectOrder:
			return 'correctly sorted with '+order
		else:
			raise Exception('Not correctly sorted')
			
	def check_get_index(self, **kargs):
		'''	used to check get_index response for contact, 
			res=${get index1}	a=2 b=1'''
		entries_list = eval(kargs['res'])['entries']
		del kargs['res']
		failedEntry = []
		for arg in kargs:
			if arg == 'other':
				prefix_count = {'prefix':'#', 'count':int(kargs[arg])}
			else:
				prefix_count = {'prefix':arg.upper(), 'count':int(kargs[arg])}
			if prefix_count not in entries_list:
				failedEntry.append(prefix_count)
		if failedEntry:
			raise Exception('cannot found: %s in entries list from result'%failedEntry)
		else:
			return 'All prefix and count are found in entries list'
		
	def _find_contacts_groups(self, resultList, findWhat):
		''' resultList = list/list_all response, findwhat = contact/group
			return big hash: contact id list / group id list'''
		contact_ids = []
		group_ids = []
		for hash in resultList:
			if hash['id'].split('/')[-2] == 'cnt':
				contact_ids.append(hash['id']) # contact id list
			if hash['id'].split('/')[-2] == 'grp':
				group_ids.append(hash['id']) # group id list
		return {'contact_ids':contact_ids, 'group_ids':group_ids}
			
	def _del_contact_or_group_list(self, result_list, delWhat, addr_id, id_hash):
		if 'contact' in delWhat:
			del_contact_kargs = {'params.addressBookId':addr_id, 'params.contactIds':id_hash['contact_ids']}
			self.del_contact(**del_contact_kargs)
		if 'group' in delWhat:
			del_group_kargs = {'params.addressBookId':addr_id, 'params.groupIds':id_hash['group_ids']}
			self.del_group(**del_group_kargs)
			
	def empty_contact_or_group_from_list(self, **kargs):
		''' res - response of list_contact
			findWhat - contact / group / contact group
			addr_id - addressbook id
		'''
		kargs['res'] = kargs['res'].replace('true','True')
		# kargs['res'] = kargs['res'].replace('null','\"None\"')
		result_list = eval(kargs['res'])['results']
		findWhat = kargs['findWhat']
		addr_id = kargs['addr_id']
		id_hash = self._find_contacts_groups(result_list, findWhat)
		self._del_contact_or_group_list(result_list, findWhat, addr_id, id_hash)
			
	def empty_contact_or_group_from_list_all(self, **kargs):
		''' res - response of list_all_contact 
			findWhat - contact / group / contact group
			* NOTE: it will empty from ALL addressbooks - for res comes from response of list_all_contact
		'''
		res_list = eval(kargs['res'])['results']
		findWhat=kargs['findWhat']
		for contact_orGroup in res_list:
			result_list = []
			addr_id = contact_orGroup['addressBookId']
			# for entries_hash in addressbook['entries']:
			result_list.append(contact_orGroup)
			
			id_hash = self._find_contacts_groups(result_list, findWhat)
			self._del_contact_or_group_list(result_list, findWhat, addr_id, id_hash)
		
	def check_dups_by_ids(self, **kargs):
		'''res comes from list_contact_dups response
			check ids list from res, ids=${id1},${id2}'''
		contacts_list = eval(kargs['res'])[0]['contacts']
		dupIDs = []
		for contact in contacts_list:
			dupIDs.append(contact['id'])
		ids = kargs['ids'].replace(' ','').split(',')
		failedFoundIds = ''
		for id in ids:
			if id not in dupIDs:
				failedFoundIds = failedFoundIds + id + ','
		if failedFoundIds:
			raise Exception('Failed to find the expeced dup id: '+failedFoundIds)
		return 'All expected dup id found'
			
	def check_dup_cnt(self, **kargs):
		if not eval(kargs['res']) and not int(kargs['expectCnt']):
			return 'Result is empty and also expect nothing'
		if not eval(kargs['res']) and int(kargs['expectCnt']):
			raise Exception('Expect %d  but got empty from res'%int(kargs['expectCnt']))
		
		else:
			resultList = eval(kargs['res'])[0]
			gotCnt = len(resultList['contacts'])
			if not gotCnt == int(kargs['expectCnt']):
				raise Exception('Expect cnt is %s but got %d'%(kargs['expectCnt'], gotCnt))
			return '%s from expect result are checked'%gotCnt
			
	def check_merge_preview_dup_fields(self, **kargs): # only check the fields which are added as new fields, the others will be returned
		kargs['res'] = kargs['res'].replace('null','\"\"')
		result_fields = eval(kargs['res'])['fields']
		failed = ''
		expectL = kargs['fields'].split('+')
		expectList = []
		checkFromNote = []
		for hashList in expectL: # expectL is multi list, each list is a contact fields list(contain field Hashes)
			for h in eval(hashList):
				expectList.append(h)
		for expectH in expectList:
			if expectH['label'] in ['title', 'department', 'company']: 
				print '%s skipped'%expectH['label']
				checkFromNote.append(expectH['label'])
			else:
				if expectH.has_key('primary'):
					del expectH['primary']
				if not expectH in result_fields:
					failed = failed + str(expectH) + ', '
		if failed:	
			raise Exception('Faild to check '+failed)
		print 'All field check from response-result-fields'
		return checkFromNote
		
	def check_merge_preview_no_dup_field(self, **kargs):
		kargs['res'] = kargs['res'].replace('null','\"\"')
		result_fields = eval(kargs['res'])['fields']
		expectL = kargs['fields'].split('+') # check new expect fields added as new fields
		failed = ''
		for expectH in expectL:
			expectH = eval(expectH)
			if expectH.has_key('primary'):
				expectH.pop('primary')
			if expectH not in result_fields:
				failed = failed + expectH + '  '
		if failed:
			failed = 'add as new field: '+failed+'\n'
		expectNoteL = kargs['notes'].split('+') # check fields added into Notes field
		for expect in expectNoteL:
			if expect not in str(result_fields[-1]):
				failed = failed + expect + '  '
		if failed:
			failed = 'notes field: '+failed	+'\n'
			raise Exception(failed)
		return 'All no-dup fields checked'
			
	def check_auto_suggest(self, **kargs):
		ids = kargs['ids']
		del kargs['ids']	
		if not isinstance(ids, list): ids = [ids]
		if ids ==[''] : ids = [ ]
		
		response = self.auto_suggest(**kargs).replace('true','\"True\"')
		contacts = eval(response)['contacts']
		gotIds = []
		for c in contacts:
			gotIds.append(c['id'])
		ids.sort()
		gotIds.sort()
		if not ids == gotIds: 
			raise Exception('expect %s but got %s'%(ids, gotIds))
		else:
			return '%s are checked from auto suggest result'%gotIds

	def empty_collected_address(self):
		'''webtop api only empty Auto-complete addressbook'''
		list_res = self.collected_address_list()
		collected_list = eval(list_res)
		ids = [contact['id'] for contact in collected_list]
		kargs = {'params.ids': ids}
		response = self.collected_address_del(**kargs)
		return 'Empty collected addresses done'
			
	def check_collect_create(self, **kargs):
		''' kargs['res'] -> the created response
			kargs['item'] -> only "address" or "id" 
			Two ways to check created result: a) expect address list 2) count of created ids
				kargs['expect_addrList'] -> if item == 'address', check created addresses by expect addr list
				kargs['id_cnt'] -> if item == 'id', check count if created ids
			'''
		got_list = eval(kargs['res'])
		item = kargs['item'] 
		got_contact_item_list = [contact_item for contact_item in [contact[item] for contact in got_list]]
		
		if item == 'address':
			expect_list = [addr.encode('utf-8') for addr in kargs['expect_addrList']]
			expect_list.sort()
			got_contact_item_list.sort()
			if not got_contact_item_list == expect_list:
				raise Exception('got addresses list from create collect result as expected addresses list')
			return '%s(s) are all checked'%item
		if item == 'id':
			if not len(got_contact_item_list) == int(kargs['id_cnt']):
				raise Exception('Expect created ids cnt is %s but got %d'%(kargs['id_cnt'], len(got_contact_item_list)))
			return got_contact_item_list
		 
	def collected_addrss_get_all(self, **kargs):
		failed = ''
		for id_addr in eval(kargs['collectRes']):
			id = id_addr['id']
			kargs = {'params.id':id}
			response = self.collected_addrss_get(**kargs)
			if not eval(response)['address'] == id_addr['address']:
				failed = failed + id + ', '
		if failed: 
			raise Exception('Failed to check id: '%failed)
		else: 
			return 'All ids and addresses are checked by COLLECTED_ADDRESS_GET'
	
	def export_contacts(self, **kargs):
		post_url = kargs['url']
		del kargs['url']
		resource_download = self.reqBuilder.buildSimpleReq(request_name='RESOURCE_DOWNLOAD_EVENTS', **kargs)
		request = 'resource.download' + resource_download
		res = self.post_to_r(request, post_url)
		if 'BEGIN:VCALENDAR' in res and 'END:VCALENDAR' in res:
			return 'Download successful'
		else: raise Exception('Download failed')