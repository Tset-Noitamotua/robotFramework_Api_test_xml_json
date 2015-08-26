# todo: add exception msg.
import sys, os
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Base import Base

class Contact(Base):
	'''
	include all contact APIs
	'''
	def __init__(self, url):
		Base.__init__(self, url)

	def list_addressbook(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_LIST', **kargs)
			return response
		except Exception, e:
			raise Exception('List addressbook failed - %s'%str(e))
			
	def list_addressbook_types(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_LIST_TYPES', **kargs)
			return response
		except Exception, e:
			raise Exception('List addressbook failed - %s'%str(e))
			
	def testType(self, s):
		return type(s)
			
	def create_addressbook(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_CREATE', **kargs)
			return str(response)
		except Exception, e:
			raise Exception('Create addressbook failed - %s'%str(e))

	def del_addressbook(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('Delete addressbook failed - %s'%str(e))
			
	def update_addressbook(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_UPDATE', **kargs)
			return response
		except Exception, e:
			raise Exception('Update addressbook failed - %s'%str(e))
			
	def get_addressbook(self, **kargs):
		try:
			response = self.request_send('ADDRESSBOOK_GET', **kargs)
			return response
		except Exception, e:
			raise Exception('Get addressbook failed - %s'%str(e))
			
	def delete_empty_trash(self):
		try:
			response = self.request_send('ADDRESSBOOK_EMPTY_TRASH')
			return response
		except Exception, e:
			raise Exception('Delete empty trash addressbook failed - %s'%str(e))

	def create_group(self, **kargs):
		try:
			response = self.request_send('GROUP_CREATE', **kargs)
			return response
		except Exception, e:
			raise Exception('Create group failed - %s'%str(e))		

	def list_group(self, **kargs):
		try:
			response = self.request_send('GROUP_LIST', **kargs)
			return response
		except Exception, e:
			raise Exception('List group failed - %s'%str(e))
	
	def del_group(self, **kargs):
		''' kargs['groupIds'] - group list to be deleted '''
		try:
			groupIds = kargs['params.groupIds']
			kargs['params.groupIds'] = []
			for gid in groupIds:
				kargs['params.groupIds'].append(gid.encode('utf-8'))

			response = self.request_send('GROUP_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('Delete group failed - %s'%str(e))	

	def rename_group(self, **kargs):
		try:
			response = self.request_send('GROUP_RENAME', **kargs)
			return response
		except Exception, e:
			raise Exception('Rename group failed - %s'%str(e))

	def add_contact_group_email(self, **kargs):
		try:
			response = self.request_send('GROUP_ADD_EMAL', **kargs)
			return response
		except Exception, e:
			raise Exception('Add group email failed - %s'%str(e))
			
	def get_group(self, **kargs):
		try:
			response = self.request_send('GROUP_GET', **kargs)
			return response
		except Exception, e:
			raise Exception('Get group failed - %s'%str(e))
	
	def list_contact(self, **kargs):
		try:
			response = self.request_send('CONTACT_LIST', **kargs)
			return response
		except Exception, e:
			raise Exception('List contact failed - %s'%str(e))
	
	def list_all_contact(self, **kargs):
		try:
			response = self.request_send('CONTACT_LIST_ALL', **kargs)
			return response
		except Exception, e:
			raise Exception('List contact failed - %s'%str(e))
	
	def del_contact(self, **kargs):
		try:
			response = self.request_send(req_name='CONTACT_DEL', **kargs)
			return 'Contact%s deleted'%kargs['params.contactIds']
		except Exception, e:
			raise Exception('Delete contact failed - %s'%str(e))

	def create_contact(self, **kargs):
		try:
			response = self.request_send('CONTACT_CREATE', **kargs)
			return response
		except Exception, e:
			raise Exception('Create contact failed - %s'%str(e))

	def create_full_contact(self, **kargs):
		try:
			request = self.reqBuilder.buildContactCreateUpdateReq('CONTACT_CREATE', True, **kargs)
			response = self.client.send(request)
			return response
		except Exception, e:
			raise Exception('Create full contact failed - %s'%str(e))

	def set_photo(self, **kargs):
		try:
			response = self.request_send('CONTACT_SETPHOTO', **kargs)
		except Exception, e:
			raise Exception('CONTACT_SETPHOTO failed - %s'%str(e))
		
	def get_contacts(self, **kargs):
		try:
			response = self.request_send('CONTACT_GET', **kargs)
			return response
		except Exception, e:
			raise Exception('get contact failed - %s'%str(e))
			
	def check_response(self, **kargs):
		utils.checkStrFromResp(expectStr=kargs['expect'], response=kargs['response'])
		
	def update_contact(self, **kargs):
		try:
			response = self.request_send('CONTACT_UPDATE', **kargs)
			return response
		except Exception, e:
			raise Exception('Update contact failed - %s'%str(e))

	def move_contact(self, **kargs):
		try:
			request = self.request_send('MOVE_CONTACT', **kargs)
			response = self.client.send(request)
		except Exception, e:
			raise Exception('Move contact failed - %s'%str(e))
			
	def add_group_contact(self, **kargs):
		try:
			response = self.request_send('GROUPCONTACT_ADD', **kargs)
			return response
		except Exception, e:
			raise Exception('Add group contact failed - %s'%str(e))	

	def del_group_contact(self, **kargs):
		try:
			response = self.request_send('GROUPCONTACT_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('Delete group contact failed - %s'%str(e))
			
			
	def auto_suggest(self, **kargs):
		try:
			response = self.request_send('SUGGEST_REQUEST', **kargs)
			return response
		except Exception, e:
			raise Exception('SUGGEST_REQUEST failed - %s'%str(e))
		
	def collected_address_list(self):
		try:
			response = self.request_send('COLLECTED_ADDRESS_LIST')
			return response
		except Exception, e:
			raise Exception('COLLECTED_ADDRESS_LIST failed - %s'%str(e))

	def collected_address_del(self, **kargs):
		try:
			response = self.request_send('COLLECTED_ADDRESS_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('COLLECTED_ADDRESS_DEL failed - %s'%str(e))
			
	def collect_autocollect_create(self, **kargs):
		try:
			response = self.request_send('COLLECTED_ADDRESS_COLLECT', **kargs)
			return response
		except Exception, e:
			raise Exception('COLLECTED_ADDRESS_COLLECT failed - %s'%str(e))

	def del_autocomplete(self, **kargs):
		'''
		input : id
		description : delete one autocomplete
		'''
		try:
			response = self.request_send('DEL_AUTOCOMPLETE', **kargs)
			return response
		except Exception, e:
			raise Exception('DEL_AUTOCOMPLETE - %s'%str(e))
			
	def collected_addrss_get(self, **kargs):
		try:
			response = self.request_send('COLLECTED_ADDRESS_GET', **kargs)
			return response
		except Exception, e:
			raise Exception('COLLECTED_ADDRESS_GET - %s'%str(e))
			
	def list_contact_dups(self, **kargs):
		try:
			response = self.request_send('LIST_DUP', **kargs)
			return response
		except Exception, e:
			raise Exception('List contact duplications failed - %s'%str(e))
			
	def list_contact_new_dups(self, **kargs):
		'''need Ids list'''
		try:
			response = self.request_send('LIST_NEW_DUP', **kargs)
			return response
		except Exception, e:
			raise Exception('LIST_NEW_DUP failed - %s'%str(e))

	def merge_preview(self, **kargs):
		try:
			response = self.request_send('PREVIEW_MERGE', **kargs)
			return response
		except Exception, e:
			raise Exception('PREVIEW_MERGE failed - %s'%str(e))
	
	def merge_all_dup(self, **kargs):
		try:
			response = self.request_send('MERGE_ALL_DUP', **kargs)
			return response
		except Exception, e:
			raise Exception('MERGE_ALL_DUP failed - %s'%str(e))
	
	def import_contact(self, **kargs):
		'''{'params': {'source': {'id': 4000333, '@resolver': 'Upload'}, 'addressBookId': 'PAB://openwave.com/webtop20/main'}, 'method': 'contacts.import'}'''
		try:
			response = self.request_send('IMPORT_CONTACT', **kargs)
			return response
		except Exception, e:
			raise Exception('IMPORT_CONTACT failed - %s'%str(e))
			
	def import_contact_UI(self, **kargs):
		'''r	contacts.import{"addressBookId":"PAB://openwave.com/webtop11/main","source":{"@resolver":"upload","id":1433401588893}}'''
		request = 'contacts.import'+str(kargs['params']).replace("'",'"')
		url = kargs['url']
		self.post_to_r(request, url)
			
	
	def contact_get_index(self, **kargs):
		try:
			response = self.request_send('CONTACT_GET_INDEX', **kargs)
			return response
		except Exception, e:
			raise Exception('Get contact index failed - %s'%str(e))	
			
			
	def create_contact_n(self, **kargs):
		n = int(kargs['amount'])
		del kargs['amount']
		for i in range(n):
			self.create_contact(**kargs)
