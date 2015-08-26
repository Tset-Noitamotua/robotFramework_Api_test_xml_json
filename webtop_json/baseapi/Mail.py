import sys, platform, os
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Base import Base
import SysUtils

class Mail(Base):
	'''
	include all mail APIs
	'''
	def __init__(self, url):
		
		Base.__init__(self, url)

	#to do throw diffrent exception
	#
	def send_mail(self, **kargs):
		try:
			response = self.request_send('MSG_SEND', **kargs)
			return response
		except Exception, e:
			raise Exception('Send mail failed - %s'%str(e))
			
	def list_mail(self, **kargs):
		try:
			response = self.request_send('MSG_HEADER_LST', **kargs)
			return response
		except Exception, e:
			raise Exception('List mail failed - %s'%str(e))
			
	def delete_mail(self, **kargs):
		try:
			response = self.request_send('MSG_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('Delete mail failed - %s'%str(e))			
		
	def move_mail(self, **kargs):
		try:
			response = self.request_send('MSG_MOVE', **kargs)
			return response
		except Exception, e:
			raise Exception('Move mail failed - %s'%str(e))

	def flag_mail(self, **kargs):
		try:
			response = self.request_send('MSG_FLAG', **kargs)
			return response
		except Exception, e:
			raise Exception('Flag mail failed - %s'%str(e))

	def report_message(self, **kargs):
		try:
			response = self.request_send('MSG_REPORT', **kargs)
			return response
		except Exception, e:
			raise Exception('Report mail failed - %s'%str(e))

	def list_mail_signature(self, **kargs):
		try:
			response = self.request_send('LIST_SIGNATURE', **kargs)
			return response
		except Exception, e:
			raise Exception('List mail signature failed - %s'%str(e))
			
	def search_mail(self, **kargs):
		try:
			response = self.request_send('VMSG_HEADER_LST', **kargs)
			return response
		except Exception, e:
			raise Exception('Search mail failed - %s'%str(e))
			
	def advanced_search_mail(self, **kargs):
		try:
			response = self.request_send('VMSG_HEADER_LST_ADVANCED', **kargs)
			return response
		except Exception, e:
			raise Exception('Advanced search mail failed - %s'%str(e))		
	
	def msg_fetch(self, **kargs):
		try:
			response = self.request_send('MSG_FETCH', **kargs)
			return response
		except Exception, e:
			raise Exception('Msg fetch failed - %s'%str(e))

	def save_draft(self,**kargs):
		saveMsgResp = self.request_send('MSG_SAVE_DRAFT', **kargs)
		return saveMsgResp
			
	def add_external_account(self, **kargs):
		try:
			accountListResp = self.request_send('EXTERNAL_MAIL_ACCOUNT',  **kargs)
			return accountListResp
		except Exception, e:
			raise Exception('Add external account failed - %s'%str(e))
			
	def update_external_account(self, **kargs):
		try:
			accountListResp = self.request_send('EXTERNAL_ACCOUNT_UPDATE',  **kargs)
			return accountListResp
		except Exception, e:
			raise Exception('Update external account failed - %s'%str(e))
			
	def list_external_account(self, **kargs):
		try:
			accountListResp = self.request_send('EXTERNAL_ACCOUNT_LIST')
			return accountListResp
		except Exception, e:
			raise Exception('List external account failed - %s'%str(e))
	
	def test_external_account(self, **kargs):
		try:
			getConnectResp = self.request_send('EXTERNAL_MAIL_ACCOUNT_TEST', **kargs)
			return getConnectResp
		except Exception, e:
			raise Exception('Test external account failed - %s'%str(e))

	def del_external_account(self, **kargs):
		try:
			res = self.request_send('EXTERNAL_ACCOUNT_DEL', **kargs)
			return res
		except Exception, e:
			raise e
	
	def create_signature(self, **kargs):
		try:
			res = self.request_send('SIGNATURE_CREATE', **kargs)
			return res
		except Exception, e:
			raise Exception('Create signature failed - %s'%str(e))
	
	def del_signature(self, **kargs):
		try:
			res = self.request_send('SIGNATURE_DEL', **kargs)
			return res
		except Exception, e:
			raise Exception('Delete signature failed - %s'%str(e))
	
	def list_signature(self):
		try:
			res = self.request_send('SIGNATURE_LIST')
			return res
		except Exception, e:
			raise Exception('List signature failed - %s'%str(e))
	
	def add_block_sender(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_ADD', **kargs)
			return res
		except Exception, e:
			raise Exception('Add block sender failed - %s'%str(e))
			
	def list_blocksender(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_LIST', **kargs)
			return res
		except Exception, e:
			raise Exception('List block sender failed - %s'%str(e))
			
	def update_blocksender(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_UPDATE', **kargs)
			return res
		except Exception, e:
			raise Exception('Update block sender failed - %s'%str(e))
			
	def disable_blocksender(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_DISABLE', **kargs)
			return res
		except Exception, e:
			raise Exception('Disable block senders failed - %s'%str(e))
			
	def enable_blocksender(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_ENABLE', **kargs)
			return res
		except Exception, e:
			raise Exception('Enable block senders failed - %s'%str(e))

	def check_sender_isblocked(self, **kargs):
		try:
			res = self.request_send('BLOCKED_SENDER_ISBLOCKED', **kargs)
			return res
		except Exception, e:
			raise Exception('Check isblocked failed - %s'%str(e))			
			
	def add_safesender(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_ADD', **kargs)
			return res
		except Exception, e:
			raise Exception('Add safe sender failed - %s'%str(e))
			
	def list_safesender(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_LIST', **kargs)
			return res
		except Exception, e:
			raise Exception('List safe sender failed - %s'%str(e))
			
	def update_safesender(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_UPDATE', **kargs)
			return res
		except Exception, e:
			raise e
			
	def disable_safesender(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_DISABLE', **kargs)
			return res
		except Exception, e:
			raise Exception('Disable allow senders failed - %s'%str(e))
			
	def enable_safesender(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_ENABLE', **kargs)
			return res
		except Exception, e:
			raise Exception('Enable allow senders failed - %s'%str(e))

	def check_sender_isallowed(self, **kargs):
		try:
			res = self.request_send('ALLOW_SENDER_ISALLOWED', **kargs)
			return res
		except Exception, e:
			raise Exception('Check isallowed failed - %s'%str(e))					
			
	
	def add_disposable_address(self, **kargs):
		try:
			res = self.request_send('ALIAS_ADD', **kargs)
			return res
		except Exception, e:
			raise Exception('Add disposable address failed - %s'%str(e))

	def list_disposable_address(self, **kargs):
		try:
			res = self.request_send('ALIAS_LIST', **kargs)
			return res
		except Exception, e:
			raise Exception('List disposable address failed - %s'%str(e))
	
	def del_disposable_address(self, **kargs):
		try:
			res = self.request_send('ALIAS_DELETE', **kargs)
			return res
		except Exception, e:
			raise Exception('Delete disposable address failed - %s'%str(e))

	def get_disposable_address(self, **kargs):
		try:
			res = self.request_send('ALIAS_GET', **kargs)
			return res
		except Exception, e:
			raise Exception('Delete disposable address failed - %s'%str(e))
			
	def update_disposable_address(self, **kargs):
		try:
			res = self.request_send('ALIAS_UPDATE', **kargs)
			return res
		except Exception, e:
			raise Exception('Delete disposable address failed - %s'%str(e))
			
	def create_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_CREATE', **kargs)
			return res
		except Exception, e:
			raise Exception('Create folder failed - %s'%str(e))
	
	def delete_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_DELETE', **kargs)
			return res
		except Exception, e:
			raise Exception('Delete folder failed - %s'%str(e))

	def list_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_LIST', **kargs)
			return res
		except Exception, e:
			raise Exception('List folder failed - %s'%str(e))
		
	def move_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_MOVE', **kargs)
			return res
		except Exception, e:
			raise Exception('Mover folder failed - %s'%str(e))

	def rename_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_RENAME', **kargs)
			return res
		except Exception, e:
			raise Exception('Rename folder failed - %s'%str(e))
	
	def empty_folder(self, **kargs):
		try:
			res = self.request_send('FOLDER_EMPTY', **kargs)
			return res
		except Exception, e:
			raise Exception('Empty folder failed - %s'%str(e))
	
	def mail_header_list_check(self, **kargs):
		try:
			res = self.request_send('MSG_HEADER_LST_CHECK', **kargs)
			return res
		except Exception, e:
			raise Exception('Msg list header check failed - %s'%str(e))
	
	def change_pwd(self, **kargs):
		try:
			res = self.request_send('USER_CHANGE_PWD', **kargs)
			return res
		except Exception, e:
			raise Exception('Change password failed - %s'%str(e))
	
	def set_timzone(self, **kargs):
		try:
			res = self.request_send('TIMEZONE_SET', **kargs)
			return res
		except Exception, e:
			raise Exception('Set timezone failed - %s'%str(e))
	
	def list_timezone(self, **kargs):
		try:
			response = self.request_send('TIMEZONE_LIST', **kargs)
			return response
		except Exception, e:
			raise Exception('List timezone failed - %s'%str(e))

	def auto_forward(self,**kargs):
		try:
			autoFwdReq = self.request_send('MAIL_FORWARDING', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('List timezone failed - %s'%str(e))
		
	def save_image_blocker(self,**kargs):
		try:
			autoFwdReq = self.request_send('IMAGE_BLOCKER_SAVE', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Save image blocker failed - %s'%str(e))

	def create_trust_sender(self,**kargs):
		try:
			autoFwdReq = self.request_send('TRUST_SENDER_CREATE', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Create image trust sender failed - %s'%str(e))
	
	def list_trust_sender(self,**kargs):
		try:
			autoFwdReq = self.request_send('TRUST_SENDER_LIST', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('List image trust sender failed - %s'%str(e))	
			
	def delete_trust_sender(self,**kargs):
		try:
			autoFwdReq = self.request_send('TRUST_SENDER_DELETE', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Delete image trust sender failed - %s'%str(e))				

	def update_trust_sender(self,**kargs):
		try:
			autoFwdReq = self.request_send('TRUST_SENDER_UPDATE', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Update image trust sender failed - %s'%str(e))			

	def get_trust_sender(self,**kargs):
		try:
			autoFwdReq = self.request_send('TRUST_SENDER_GET', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Get image trust sender failed - %s'%str(e))
			
	def send_receipt(self, **kargs):
		try:
			autoFwdReq = self.request_send('SEND_RECEIPT', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Send receipt failed - %s'%str(e))
	'''	
	def ignore_receipt(self, **kargs):
		try:
			autoFwdReq = self.request_send('IGNORE_RECEIPT', **kargs)
			return autoFwdReq
		except Exception, e:
			raise Exception('Ignore receipt failed - %s'%str(e))
	'''
	def set_auto_reply(self, **kargs):
		try:
			res = self.request_send('MAIL_AUTO_REPLY', **kargs)
			return res
		except Exception, e:
			raise Exception('Set auto reply failed. - %s'%str(e))

	def disable_auto_reply(self, **kargs):
		try:
			res = self.request_send('MAIL_AUTO_REPLY_DISABLE', **kargs)
			return res
		except Exception, e:
			raise Exception('Disable auto reply failed. - %s'%str(e))

	def set_auto_reply_cpms(self, **kargs):
		try:
			if kargs.has_key('endday'):
				kargs['endDate'] = SysUtils.getEndTime(plus=kargs['endday'])
			print kargs
			request = self.reqBuilder.buildAutoReplyReq('MAIL_AUTO_REPLY_CPMS', True, **kargs)
			res = self.client.send(request)
			return res
		except Exception, e:
			raise Exception('Set auto reply (CPMS) failed. - %s'%str(e))

	def disable_auto_reply_cpms(self, **kargs):
		try:
			res = self.request_send('MAIL_AUTO_REPLY_DISABLE_CPMS', **kargs)
			return res
		except Exception, e:
			raise Exception('Disable auto reply failed. - %s'%str(e))
			
	def load_auto_reply(self, **kargs):
		try:
			res = self.request_send('AUTO_REPLY_LOAD', **kargs)
			return res
		except Exception, e:
			print str(e)
			raise Exception('Failed to load from AUTO_REPLY_LOAD')
			
	def get_quota(self, **kargs):
		try:
			res = self.request_send('MAIL_GET_QUOTA', **kargs)
			return res
		except Exception, e:
			raise Exception('Get quota failed - %s'%str(e))

	def save_mobile_signature(self, **kargs):
		try:
			print kargs
			res = self.request_send('MOBILE_SIGNATURE_CREATE', **kargs)
			return res
		except Exception, e:
			raise Exception('Save mobile signature failed - %s'%str(e))

	def load_mobile_signature(self, **kargs):
		try:
			res = self.request_send('MOBILE_SIGNATURE_LOAD', **kargs)
			return res
		except Exception, e:
			raise Exception('Load mobile signature failed - %s'%str(e))

	def add_group_email(self, **kargs):
		try:
			res = self.client.send('<request><contacts action="add_group_email" addressBookId="PAB://openwave.com/webtop2/main" group_id="PAB://openwave.com/webtop2/main/grp/GROUP_217" email="webtop8@openwave.com"></contacts></request>')
			return res
		except Exception, e:
			raise Exception('Add group email failed. - %s'%str(e))
	
if __name__=='__main__':
	#mailobj = Mail('http://rwc-hinoki06.owmessaging.com:8080/kiwi-octane-rel/dd')
	#test = mailobj.send_mail(body=4, to='888')
	print 'test'