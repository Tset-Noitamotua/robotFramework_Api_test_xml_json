import sys, re, json, os
sys.path.append(os.path.join('..', 'const'))
sys.path.append(os.path.join('..', 'util'))
sys.path.append(os.path.join('..', 'exception'))
import MsgConsts, SysUtils
from TestCodeException import TestCodeException



# Key consts
key_res_error = 'error'

#mail
expr_mail_id_subject = '"uid": ([0-9]+).*?"subject": "%s"'
expr_mail_id = '"uid": ([0-9]+)'
expr_subject_headerlist_res = '"subject": "(.*)"'
expr_receive_date_headerlist_res = '"receivedDate": ([0-9]+)'

def string_to_json_utf8(String):
	String='''{
	  "jsonrpc" : "2.0",
	  "id" : null,
	  "result" : {
		"@type" : "Contact",
		"id" : "PAB://openwave.com/webtop8/main/cnt/CONTACT_123",
		"firstName" : "testFirst",
		"lastName" : "testLast",
		"email" : "home@test.com",
		"fields" : [ {
		  "label" : "home",
		  "type" : "lzEmail",
		  "value" : "home@test.com"
		}, 
		{
		  "label" : "work",
		  "type" : "lzEmail",
		  "value" : "work@test.com"
		} ],
		"modifiedTime" : 0
	  },
	  "procTime" : 31
	}'''
	
	
	

def listALLItem(expr_key, res, exception_when_not_found=False):
	'''
	expr_key:expression str
	res: xml response
	exception_when_not_found:nothing found in res,exception will be raised if exception_when_not_found=True
	'''
	#res.replace('><','>\n<')
	result_list = SysUtils.findAll(expr_key, res)
	if exception_when_not_found and (len(result_list) == 0):
		raise TestCodeException(MsgConsts.MAIL_NO_KEY_FOUND%expr_key)
	return result_list

#key with params
def listAll(expr_key, res, *args):
	expr_key = expr_key%args
	return listALLItem(expr_key, res)

def isResError(res):
	return (key_res_error in res)

# def getResErrorCode(res):
	# codelist = listALLItem(expr_error_code, res, True)
	# return codelist[0]

#mail
# contact


def getIdListByName(name='', res='', all=False):
	''' This could only be use as DICT of res
		res = {
	  "jsonrpc" : "2.0",
	  "id" : null,
	  "result" : [ {
		"id" : "PAB://openwave.com/webtop7/main",
		"name" : "Default",
		"type" : "Webtop",
		"properties" : {
		  "default" : "true",
		  "private" : "true"
		}
	  } ],
		"procTime" : 15
		name : addressbook name
	'''
	if type(res) is unicode or type(res) is str: 
		print type(res)
		resJn = eval(res.replace('\n',''))
	else: resJn = res
	idList = []
	for i in resJn:
		if all:
			if i.has_key('id'): idName = 'id'
			elif i.has_key('uid'): idName = 'uid'
			id = str(i[idName])
			idList.append(id)
		elif i['name']==name:
			id = str(i['id'])
			idList.append(id)
	return idList
	
def getCreatedIdFromRes(**kargs):
	''' kargs['firstName'] = testFirst
		kargs['res'] - This could only be use as HASH of res
			kargs['res']={
			"id" : "PAB://openwave.com/webtop7/main-762005248-16447--921",
			"name" : "1421042055",
			"type" : "Webtop",
			"properties" : { }
	  }'''
	kargs['res'] = kargs['res'].replace('true','True')
	if type(eval(kargs['res'])) == list:
		res = eval(kargs['res'])
		del kargs['res']
		id = ''
		for hash in res:
			if hash[kargs.keys()[0]] == kargs[kargs.keys()[0]]:
				return hash['id']
		if not id:
			raise Exception('name cannot be found')
		
		
	else:	
		resJn = eval(kargs['res'])
		del kargs['res'] # make kargs only left name pair	
		item_name = kargs.keys()[0] #  ='firstName'
		item_name_value = kargs[item_name]
		
		if resJn.has_key(item_name) and resJn[item_name] == item_name_value:
			return resJn['id']
		else:
			raise Exception('no %s - %s found in %s'%(item_name,item_name_value,resJn ) )
	
	
def getMailIDListBySubject(subject, res):
	return listAll(expr_mail_id_subject, res, subject)

def getMailIDList(res):
	'''res is mailheadlist response'''
	print 'in getMailIDList'
	return listAll(expr_mail_id, res)

def getFlagValueByMailID(mail_id, flag_name, res):
	result_obj = json.loads(res)
	for mail in result_obj['messages']:
		if str(mail['uid']) == mail_id:
			if mail['flags'].has_key(flag_name):
				return mail['flags'][flag_name]
	return None
	
def getMailSubjectFromMsgListRes(header_list_res):
	return listAll(expr_subject_headerlist_res, header_list_res)
	
def getMailReceivedDateFromMsgListRes(header_list_res):
	return listAll(expr_receive_date_headerlist_res, header_list_res)

def getMailFlaggedFromMsgListRes(header_list_res):
	result_obj = json.loads(header_list_res)
	flag_list=[]
	for mail in result_obj['messages']:
		if mail['flags'].has_key('flagged'):
			flag_list.append(mail['flags']['flagged'])
		else:
			flag_list.append(False)
	return flag_list
	
def getReturnReceiptValsFromFetchRes(fetch_res):
	result_obj = json.loads(fetch_res)
	if result_obj.has_key('promptReturnReceipt'):
		return result_obj['promptReturnReceipt'] == str(True)
	else:
		return False
		
def getAnsweredValByMailID(header_list_res, mail_id):
	result_obj = json.loads(header_list_res)
	flag_list=[]
	for mail in result_obj['messages']:
		if (str(mail['uid']) == mail_id):
			if mail['flags'].has_key('answered'):
				return mail['flags']['answered'] == str(True)
			else:
				return False
	raise Exception('Can not find answered flag for mail %s'%mail_id)
	
def getForwardedValByMailID(header_list_res, mail_id):
	result_obj = json.loads(header_list_res)
	flag_list=[]
	for mail in result_obj['messages']:
		if (str(mail['uid']) == mail_id):
			if mail['flags'].has_key('forwarded'):
				return mail['flags']['forwarded'] == str(True)
			else:
				return False
	raise Exception('Can not find forwarded flag for mail %s'%mail_id)
	
def getFolderListFromListRes(list_folder_res):
	result_obj = json.loads(list_folder_res)
	folder_list=[]
	for folder in result_obj['subfolders']:
		folder_list.append(folder['path'])
	return folder_list
	
def getFolderListByFullName(folder_full_path, list_folder_res):
	result_obj = json.loads(list_folder_res)
	result = []
	matchFolders(folder_full_path, result_obj['subfolders'], result)
	return result
	
def matchFolders(folder_full_path, folder_list, result):
	for folder in folder_list:
		if folder['path'] == folder_full_path:
			result.append(folder['name'])
		else:
			if folder.has_key('subfolders'):
				matchFolders(folder_full_path, folder['subfolders'], result)

def	getMailsByFolderFromSearchRes(folderPaths, search_res):
	result_obj = json.loads(search_res)
	result = []
	if folderPaths == []:
		for msg in result_obj['messages']:
			result.append(msg["uid"])
	else:		
		for msg in result_obj['messages']:
			print msg["folderPath"] in folderPaths
			if msg["folderPath"] in folderPaths:
				result.append(msg["uid"])
	return result
	
def getMailListByFromName(name, res):
	result_obj = json.loads(res)
	result = []
	for msg in result_obj['messages']:
		if msg['from'].has_key('name'):
			if msg['from']['name'] == name:
				result.append(msg['uid'])			
	return result
	
def getSignatureIDList(res):
	result_obj = json.loads(res)
	result = []
	for signature in result_obj:
		result.append(signature['id'])
	return result
	
def getExternalAccIDs(res):
	result_obj = json.loads(res)
	result = []
	for account in result_obj:
		result.append(account['id'])
	return result
	
def getExternalAccCont(username, accountListResp):
	result_obj = json.loads(accountListResp)
	result = []
	for account in result_obj:
		if account['username'] == username:
			result.append(json.dumps(account))
	return result

def getSignatureIDByLabel(label, res):
	result_obj = json.loads(res)
	result = []
	for signature in result_obj:
		if signature['label'] == label:
			result.append(signature['id'])
	return result	

def getExternalAccIDByUserName(username, accountListResp):
	result_obj = json.loads(accountListResp)
	result = []
	for account in result_obj:
		if account['username'] == username:
			result.append(account['id'])
	return result
	
def getTimezoneIDList(list_tz_res):
	tz_list = json.loads(list_tz_res)
	result = []
	for account in tz_list:
		result.append(account['id'])
	return result	
	
def getDateValueBySubjectAndFieldName(resp,  field_name, subject):
	msg_result_map = json.loads(resp)
	result = []
	for msg in msg_result_map['messages']:
		if msg['subject'] == subject:
			result.append(msg[field_name])
	return result

def getDateValueFromFetchRes(resp,  field_name, subject):
	msg_result_map = json.loads(resp)
	result = []
	if msg_result_map['subject'] == subject:
		result.append(msg_result_map[field_name])
	return result

def __getGmtFromName(tz_name):
	return tz_name.split(']')[0].split('[')[1]

def getTimezoneMap(tz_res):
	tz_list = json.loads(tz_res)
	map_result = {}
	for tz in tz_list:
		result_gmt_key = __getGmtFromName(tz['name'])
		if map_result.has_key(result_gmt_key):
			map_result.get(result_gmt_key).append(tz['id'])
		else:
			map_result[result_gmt_key] = [tz['id']]
	return map_result

'''
	timezone_ids = listAll(expr_get_timezone_id, res)
	timezone_names = listAll(expr_get_timezone_name_gmt, res)
	if len(timezone_ids) != len(timezone_names):
		raise Exception('The number(%s) of timezone ID is different with the number(%s) of timezone name.'%(len(timezone_ids), len(timezone_names)))
	map_result = {}
	for i in range(0, len(timezone_names)):
		gmt_key = timezone_names[i]
		if map_result.has_key(gmt_key):
			map_result.get(gmt_key).append(timezone_ids[i])
		else:
			map_result[gmt_key] = [timezone_ids[i]]
	return map_result

'''

def getEventContentBySummary(summary, report_res):
	event_list = json.loads(report_res)
	event_lst_result = []
	for event in event_list['events']['results']:
		if event['summary'] == str(summary):
			event_lst_result.append(event)
	return event_lst_result
	
def getEventIDBySummary(summary, report_res):
	event_list = json.loads(report_res)
	event_lst_result = []
	for event in event_list['events']['results']:
		if (event['summary'] == str(summary)) and event.has_key('recurrenceOf'):
			event_lst_result.append(event['uid'])
	return event_lst_result
	
def getEventMasterIDBySummary(summary, report_res):
	event_list = json.loads(report_res)
	event_lst_result = []
	for event in event_list['events']['results']:
		if event['summary'] == str(summary):
			if event.has_key('recurrenceOf'):
				return event['recurrenceOf']
	return None