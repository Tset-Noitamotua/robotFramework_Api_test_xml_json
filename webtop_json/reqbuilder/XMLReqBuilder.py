import sys, platform, os
sys.path.append(os.path.join('..', 'util'))
sys.path.append(os.path.join('..', 'common'))
import SysUtils, re
from AbstractReqBuilder import AbstractReqBuilder

class XMLReqBuilder(AbstractReqBuilder):
	'''
	include all request build method: buildSimpleReq, buildSpecialReq
	include all XML related method
	'''
	def buildSimpleReq(self, request_name, use_default_param=True, del_empty_field=True, **args):
		#get request str by request name
		req_str = SysUtils.getReqByName(request_name)
		#replace with default params
		if use_default_param:
			req_str = self.__createReqDefaultVals(req_str, SysUtils.getDefaultParams(request_name))
		#replace with final params: key=%s and <key>%s</key>
		req_str = self.__createReqFinalVals(req_str, args)
		#delete empty request field like xxx=%s or <aa>%s</aaa>
		if del_empty_field:
			req_str = self.__delEmptyReqFields(req_str)
			req_str = self.__delEmptyOtherPlaceHolder(req_str)
			req_str = self.__delEmptyXMLNode(req_str)
		print req_str
		return req_str

	def __createReqDefaultVals(self, req_str, params):
		for key, value in params.items():
			req_str = req_str.replace(' ' + key + '="%s',' ' + key + '="'+str(value)).replace('<' + key + '>%s</' + key + '>', '<' + key + '>' + str(value) + '</' + key + '>')
		return req_str

	def __createReqFinalVals(self, req_str, params):
		''' name=%s
			>%s<'''
		for key, value in params.items():
			req_str = re.sub(' ' + key + '="[^"]*"', ' ' + key + "='" + str(value) + "' ", req_str)
			req_str = re.sub('<' + key + '>.*</' + key + '>', '<' + key + '>' + str(value) + '</' + key + '>', req_str)
		return req_str

	def __delEmptyReqFields(self, req_str):
		req_str = re.sub(' [a-zA-Z-]+="%s"', '', req_str)
		req_str = re.sub('<[a-zA-Z-]+>%s</[a-zA-Z-]+>', '', req_str)
		return req_str
		
	def __delEmptyOtherPlaceHolder(self, req_str):
		req_str = re.sub('%s', '', req_str)#may have problems
		return req_str
	
	def __delEmptyXMLNode(self, req_str):
		req_str = re.sub('<[a-zA-Z]+ />', '', req_str)#may have problems
		return req_str
		
	def buildPrefRequest(self, use_default_param=False, **param_dict):
		'''
		special for preference setting
		<request><prefs action="set"></prefs></request>
		'''
		sub_req_str = SysUtils.getReqByName('SUB_PREF')
		sub_req = ''
		if use_default_param:
			for (key, value) in SysUtils.getDefaultParams('SUB_PREF').items():
				sub_req = sub_req + sub_req_str%(key, value)
		else:
			print param_dict
			for key, value in param_dict.items():
				sub_req = sub_req + sub_req_str%(key, value)
		
		req_str = SysUtils.getReqByName('PREF_SET')
		return req_str%sub_req

	def buildMailPrefrenceRequest(self, use_default_param=False, **param_dict):
		'''
		<mailPreference action="save"><mailpreference %s="%s" /></mailPreference>
		'''
		sub_req_str = SysUtils.getReqByName('SUB_MAIL_PREFERRENCE')
		sub_req = ''
		if use_default_param:
			for (key, value) in SysUtils.getDefaultParams('SUB_MAIL_PREFERRENCE').items():
				sub_req = sub_req + sub_req_str%(key, value)
		else:
			print param_dict
			for key, value in param_dict.items():
				sub_req = sub_req + sub_req_str%(key, value)
		
		req_str = SysUtils.getReqByName('MAIL_PREFERENCE_SAVE')
		return req_str%sub_req

	def buildMobileMailPrefrenceRequest(self, use_default_param=False, **param_dict):
		'''
		<request><mobileMailPreference action="save">%s</mobileMailPreference></request>
		'''
		sub_req_str = SysUtils.getReqByName('MOBILE_SUB_MAIL_PREFERRENCE')
		sub_req = ''
		if use_default_param:
			for (key, value) in SysUtils.getDefaultParams('MOBILE_SUB_MAIL_PREFERRENCE').items():
				sub_req = sub_req + sub_req_str%(key, value)
		else:
			print param_dict
			for key, value in param_dict.items():
				sub_req = sub_req + sub_req_str%(key, value)
		
		req_str = SysUtils.getReqByName('MOBILE_MAIL_PREFERENCE_SAVE')
		return req_str%sub_req
		
	def buildBlockSenderBatchRemoveReq(self, use_default_param=False, *blocksender):
		remove = ''
		for sender in blocksender:
			remove = remove + SysUtils.getReqByName('BLOCK_SENDER_REMOVE_NODE')%sender
		return SysUtils.getReqByName('BLOCK_SENDER_CTNR')%remove

	def buildSafeSenderBatchRemoveReq(self, use_default_param=False, *blocksender):
		remove = ''
		for sender in blocksender:
			remove = remove + SysUtils.getReqByName('SAFE_SENDER_REMOVE_NODE')%sender
		return SysUtils.getReqByName('SAFE_SENDER_CTNR')%remove
		
	def buildContactCreateUpdateReq(self, request_name, use_default_param=False, **param_dict):
		'''
		build request for create/update contact and vcard body
		'''
		sub_req_str = SysUtils.getReqByName('CONTACT_FIELD')
		ctnr_req_str = SysUtils.getReqByName(request_name)
		sub_req = ''
		req_str = ctnr_req_str
		#deal with contactFields
		if param_dict.has_key('contactFields'):
			for each_contact_field in param_dict['contactFields']:
				sub_req = sub_req + self.__createReqDefaultVals(sub_req_str, each_contact_field)
			param_dict.pop('contactFields')#this param will be used later
		else:
			if use_default_param:
				#deal with contactFields format
				default_params_dict = SysUtils.getDefaultParams('CONTACT_CREATE')
				if default_params_dict.has_key('contactFields'):
					for each_contact_field in default_params_dict['contactFields']:
						sub_req = sub_req + self.__createReqDefaultVals(sub_req_str, each_contact_field)
		sub_req = self.__delEmptyReqFields(sub_req)#no need for this,maybe
		#deal with common params
		#default params
		if use_default_param:
			default_params_dict = SysUtils.getDefaultParams('CONTACT_CREATE')
			if default_params_dict.has_key('contactFields'):
				default_params_dict.pop('contactFields')
			req_str = self.__createReqDefaultVals(ctnr_req_str, default_params_dict)
		#user params 
		req_str = self.__createReqFinalVals(req_str, param_dict)
		#empty fields
		req_str = self.__delEmptyReqFields(req_str%sub_req)
		return req_str
		
	def buildDelBatchAuotocompleteReq(self, use_default_param=False, *id_list):
		remove = ''
		for auto_id in id_list:
			remove = remove + SysUtils.getReqByName('DEL_AUTOCOMPLETE_NODE')%auto_id
		return SysUtils.getReqByName('DEL_AUTOCOMPLETE_CTNR')%remove
	
	def buildGetContactsReq(self, use_default_param=False, **kargs):
		sub_req = ''
		id_list = []
		if kargs.has_key('id_list'):
			id_list = kargs['id_list']
			kargs.pop('id_list')
		req_str = self.__createReqFinalVals(SysUtils.getReqByName('GET_CONTACT_CTNR'), kargs)
		for contact_id in id_list:
			sub_req = sub_req + SysUtils.getReqByName('GET_CONTACT_NODE')%contact_id
		return req_str%sub_req

	def buildPreviewMergeReq(self, use_default_param=False, **kargs):#similar with buildGetContactsReq
		sub_req = ''
		id_list = []
		if kargs.has_key('id_list'):
			id_list = kargs['id_list']
			kargs.pop('id_list')
		req_str = self.__createReqFinalVals(SysUtils.getReqByName('PREVIEW_MERGE_CTNR'), kargs)
		for contact_id in id_list:
			sub_req = sub_req + SysUtils.getReqByName('PREVIEW_MERGE_NODE')%contact_id
		return req_str%sub_req

	def buildCreateUpdateEventReq(self, request_name, use_default_param=False, **kargs):
		req_str = SysUtils.getReqByName(request_name)
		#format request with default params(no default attendees)
		if use_default_param:
			param_dict = SysUtils.getDefaultParams(request_name)
			req_str = self.__createReqDefaultVals(req_str, param_dict)
			print param_dict
		#format request with user params
		req_str = self.__createReqFinalVals(req_str, kargs)
		req_str = self.__delEmptyReqFields(req_str)#empty all %s field except placeholder-%s for attendees
		#format with atandee, if there is any
		sub_req = ''
		if kargs.has_key('attendees'):
			node_req = SysUtils.getReqByName('EVENT_CREATE_ATTENDEE')
			attendee_param = SysUtils.getDefaultParams('EVENT_CREATE_ATTENDEE')
			for each_attendee in kargs['attendees']:
				node_req = self.__createReqDefaultVals(node_req, attendee_param) 
				sub_req = sub_req + self.__createReqFinalVals(node_req, each_attendee)
		#format ctnr with sub_req(attendees)
		req_str = req_str%sub_req
		return req_str
	
	#please don't mod this method, it's exactly same with 'buildCreateEventReq' except request name.
	def buildEventInviteReq(self, use_default_param=False, **kargs):
		req_str = SysUtils.getReqByName('EVENT_SEND_INVITE')
		#format request with default params(no default attendees)
		if use_default_param:
			param_dict = SysUtils.getDefaultParams('EVENT_SEND_INVITE')
			req_str = self.__createReqDefaultVals(req_str, param_dict)
			print param_dict
		#format request with user params
		req_str = self.__createReqFinalVals(req_str, kargs)
		req_str = self.__delEmptyReqFields(req_str)#empty all %s field except placeholder-%s for attendees
		#format with atandee, if there is any
		sub_req = ''
		if kargs.has_key('attendees'):
			node_req = SysUtils.getReqByName('EVENT_CREATE_ATTENDEE')
			attendee_param = SysUtils.getDefaultParams('EVENT_CREATE_ATTENDEE')
			for each_attendee in kargs['attendees']:
				node_req = self.__createReqDefaultVals(node_req, attendee_param) 
				sub_req = sub_req + self.__createReqFinalVals(node_req, each_attendee)
		#format ctnr with sub_req(attendees)
		req_str = req_str%sub_req
		return req_str
		
	def buildGetIndexReq(self, use_default_param=False, **kargs):
		req_str = SysUtils.getReqByName('CONTACT_GETINDEX')
		return req_str%(kargs['addressBookId'],kargs['field'])
		
	def buildAutoReplyReq(self, request_name='MAIL_AUTO_REPLY_CPMS',use_default_param=False, endday='2', **kargs):
		req_str = SysUtils.getReqByName(request_name)
		if use_default_param:
			param_dict = SysUtils.getDefaultParams(request_name)
			req_str = self.__createReqDefaultVals(req_str, param_dict)
		# if not use_default_param:
			# param_dict['endDate'] = SysUtils.getEndTime(kargs['endday'])
		
		req_str = self.__createReqFinalVals(req_str, kargs)
		req_str = self.__delEmptyReqFields(req_str)
		
		sub_req = ''
		optionsNode = ''
		if kargs.has_key('option'):
			for opt in eval(kargs['option']):
				kargs_dict = opt
				sub_req = '<option name="%s" value="%s"/>'
				sub_req = sub_req%(kargs_dict['name'], kargs_dict['value'])
				optionsNode = optionsNode + sub_req
			#format with atandee, if there is any
		#format ctnr with sub_req(attendees)
		req_str = req_str%('<options>' + optionsNode + '</options>')
		return req_str
		
		
		
		
		
		
		
		
if __name__=='__main__':
	reqbuilder = XMLRequestBuilder()
	test = reqbuilder.buildSimpleReq('msgsendRequest', True, body=4, to='888')
	print test