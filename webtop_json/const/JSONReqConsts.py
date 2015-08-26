#bug : change '="%s">' to '="%s" >', or the parameter won't be replaced
#attention: avoid user " in default parameters

# Login
# LOGIN = {"method":"user.login","params":{"username" : "", "password" : ""}}
LOGIN = {"method":"auth.login","params":{"username" : "", "password" : ""}}
LOGOUT = {"method":"auth.logout","params":{}}

# Mail
#mail setting get quota
MAIL_GET_QUOTA= {"method":"mail.message.getQuota","params":{ "accountId" : ""}}

MSG_HEADER_LST = {"method":"mail.message.list", "params":{"accountId" : "", "folderPath" : "", "uidnext" : "", "sort" : {"field" : "natural","direction" : "descending"}, "page" : {"offset" : 0,  "size" : 20}, "uidPage" : None, "recipients" : "", "thread" : "false", }}

MSG_SEND = {"method":"mail.message.send", "params":{"accountId": "", "from": "", "to": "", "recipients": {}, "cc": "", "bcc": "", "subject": "", "body": "", "bodyType": "plain", "attachments": [], "priority": "", "inReplyTo": "", "references": "", "flagForwarded": None, "flagAnswered": None, "saveInSent": "", "requestMdn": "", "draftUidsToDelete": []}}
#got internal error if bodytype not in[plain, html, flash-html]

VMSG_HEADER_LST = {"method":"mail.message.search", "params":{"accountId" : "", "folderPaths" : "", "subfolders" : "true", "terms" : "", "fields" : [ "from", "body", "subject", "recipients" ], "sort" : {"field" : "priority", "direction" : "descending"}, "count" : "20"}}
#sort can not be empty?
#GOT ENTERNAL ERROR???

MSG_HEADER_LST_CHECK = {"method":"mail.message.check", "params":{"accountId" : None, "folderPath" : "INBOX", "uidnext" : "", "sort" : {  "field" : "natural","direction" : "descending"}, "recipients" : 'false', "thread" : 'false'}}

MSG_FETCH = {"method" : "mail.message.get", "params" : {"accountId" : "", "folderPath" : "INBOX", "messageUid" : "", "partPath" : None, "format" : "plaintext", "images" : "none", "flagSeen" : "", "truncate" : "true"}}
#partPath can't be ""
MSG_MOVE = {"method":"mail.message.move", "params":{"accountId" : "", "folderPath" : "", "selection" : "", "destFolderPath" : ""}}
MSG_FLAG = {"method":"mail.message.flag", "params":{"accountId" : "", "folderPath" : "", "selection" : "", "flag" : [], "value" : ""}}
MSG_REPORT = {"method":"mail.message.report", "params":{"accountId" : "", "folderPath" : "", "selection" : [], "type" : "junk", "destFolderPath" : "Trash"}}
MSG_SAVE_DRAFT = {"method":"mail.message.saveDraft", "params":{"accountId" : "", "from" : "", "recipients" : {}, "to" : "", "cc" : "", "bcc" : "", "subject" : "", "body" : "", "bodyType" : "plain", "attachments" : [], "priority" : "", "inReplyTo" : "", "references" : None, "draftProperties" : None, "draftUidsToDelete" : []}}

MSG_DEL = {"method":"mail.message.delete", "params":{"accountId" : "", "folderPath" : "", "selection" : []}}

VMSG_HEADER_LST_ADVANCED={"method":"mail.message.advancedSearch", "params":{"accountId" : "", "folderPaths" : [], "subfolders" : "true", "recipient" : None, "sender" : None, "subject" : None, "body" : None, "before" : None, "after" : None, "sort" : {"field" : "subject",  "direction" : "ascending"}, "count" : 20}}

SEND_RECEIPT = {"method":"mail.message.processMdnRequest", "params":{"accountId" : None, "folderPath" : "", "uid" : "", "acknowledge" : ""}}
#IGNORE_RECEIPT = '<request><mail action="ignorereceipt" uid="%s" accountId="" folder="INBOX"></mail></request>'
# Folder
FOLDER_CREATE = {"method":"mail.folder.create", "params":{"accountId" : None, "parentPath" : "", "name" : ""}}
FOLDER_LIST = {"method":"mail.folder.list", "params":{"accountId" : None, "folderPath" : "", "depth" : 1, "details" : "false", "createSpecialFolder" : "true"}}
FOLDER_MOVE = {"method":"mail.folder.move", "params":{"accountId" : None, "folderPaths" : [], "newParentPath" : ""}}
FOLDER_RENAME = {"method":"mail.folder.rename", "params":{"accountId" : None, "folderPath" : "", "newName" : ""}}
FOLDER_DELETE = {"method":"mail.folder.delete", "params":{"accountId" : None, "folderPaths" : []}}
FOLDER_EMPTY = {"method":"mail.folder.empty", "params":{"accountId" : "", "folderPath" : ""}}

#block sender
BLOCKED_SENDER_DISABLE = {"method":"mail.blockedSender.disable", "params":{}}
BLOCKED_SENDER_ENABLE = {"method":"mail.blockedSender.enable", "params":{}}
BLOCKED_SENDER_UPDATE = {"method":"mail.blockedSender.modify", "params":{"add" : [], "remove" : []}}
BLOCKED_SENDER_ISBLOCKED = {"method":"mail.blockedSender.isBlocked", "params":{"sender" : ""}}
BLOCKED_SENDER_LIST = {"method":"mail.blockedSender.load", "params":{}}
BLOCKED_SENDER_ADD = {"method":"mail.blockedSender.save", "params":{"object" : {"enabled" : "true", "senders" : []}}}
#allow sender
ALLOW_SENDER_DISABLE = {"method":"mail.allowedSender.disable", "params":{}}
ALLOW_SENDER_ENABLE = {"method":"mail.allowedSender.enable", "params":{}}
ALLOW_SENDER_UPDATE = {"method":"mail.allowedSender.modify", "params":{"add" : [], "remove" : []}}
ALLOW_SENDER_ISALLOWED = {"method":"mail.allowedSender.isAllowed", "params":{"sender" : ""}}
ALLOW_SENDER_LIST = {"method":"mail.allowedSender.load", "params":{}}
ALLOW_SENDER_ADD = {"method":"mail.allowedSender.save", "params":{"object" : {"enabled" : "true", "senders" : []}}}

#signature
SIGNATURE_CREATE = {"method":"mail.signature.create", "params":{"object" : {"label" : "default signature", "contentType" : "text/plain", "text" : "default signature", "default" : 'true'}}}
SIGNATURE_LIST = {"method":"mail.signature.list", "params":{}}
SIGNATURE_DEL = {"method":"mail.signature.delete", "params":{"ids" : []}}
SIGNATURE_GET = {"method":"mail.signature.get", "params":{"id" : ""}}
SIGNATURE_UPDATE = {"method":"mail.signature.update", "params":{"object" : {"id" : "", "label" : "default signature", "contentType" : "text/plain", "text" : "default signature", "default" : "true"}}}

#mobile signature
MOBILE_SIGNATURE_CREATE = {"method":"mail.mobileSignature.save", "params":{"object" : {"label" : "default signature", "contentType" : "text/plain", "text" : "default signature", "default" : 'true'}}}
MOBILE_SIGNATURE_LOAD = {"method":"mail.mobileSignature.load", "params":{}}


MAIL_FORWARDING = {"method":"mail.forwarding.save", "params":{ "object" : { "sendAsAttachment" : 'false', "enabled" : "true", "keepCopy" : "false", "addresses" : []}}}

PREFS_SET_TEMPLATE = {"method":"prefs.set", "params":{"map" : {}}}
PREFS_SET_MAIL = '''<request>
				<prefs action="set">
				<prefs name="attr.user.mail.SendFormat">plain</prefs>
				<prefs name="attr.user.mail.AutoSaveDraftFlag">false</prefs>
				<prefs name="attr.user.mail.SaveToDraftsInterval">60</prefs>
				<prefs name="attr.user.mail.ReplyPrefix">-</prefs>
				<prefs name="autoCreateContact">true</prefs>
				<prefs name="attr.user.mail.disableReloadOnDelete">false</prefs>
				<prefs name="attr.user.mail.readFirstMail">false</prefs>
				<prefs name="attr.user.mail.ViewMode"/>
				<prefs name="attr.user.mail.IsConversation"/>
				<prefs name="attr.user.mail.TimeDisplayFormat">short</prefs>
				</prefs></request>'''

PREFS_EMPTY_TRASH_WHEN_LOGOUT = '<request><mailPreference action="save"><mailpreference emptyTrashOnLogout="%s" /></mailPreference></request>'
SAVE_OUTGOING_MSG = '<request><mailPreference action="save"><mailpreference saveOutgoingMessages="%s" autoCheckInterval="%s" replyQuoting="%s" /></mailPreference></request>'				

#external account		
EXTERNAL_MAIL_ACCOUNT = {
    'params': {
        'object': {
            'username': 'new.swisscom@yahoo.com',
            'protocol': 'imap',
            'accountFromName': 'accountfromname',
            'imapJunkFolder': 'Junk',
            'imapTrashFolder': 'Trash',
            'autoCheckInterval': '0',
            'accountReplyTo': '',
            'id': '',
            'port': '993',
            'smtpUser': '',
            'accountOrder': '0',
            'accountName': 'accountname',
            'smtpHost': 'smtp.mail.yahoo.com',
            'imapDraftsFolder': 'Drafts',
            'keepExternalMessages': 'true',
            'smtpUseAuthentication': 'true',
            'accountEmail': 'new.swisscom@yahoo.com',
            'signatureId': '',
            'imapSentFolder': 'Sent',
            'securityType': 'SSL',
            'host': 'imap.mail.yahoo.com',
            'password': 'laszlo123',
            'sendFromMainAccount': 'true',
            'smtpPassword': '',
            'smtpSecurityType': 'SSL',
            'checkOnStartup': 'true',
            'smtpUseMainCredentials': 'false',
            'useAuthentication': 'false',
            'smtpPort': '465',
            'accountFromEmail': 'new.swisscom@yahoo.com'
        }
    },
    'method': 'mail.externalAccount.create'
}







EXTERNAL_MAIL_ACCOUNT_TEST = {
    'params': {
        'account': {
            'username': 'new.swisscom@yahoo.com',
            'protocol': 'imap',
            'accountFromName': 'accountfromname',
            'imapJunkFolder': 'Junk',
            'imapTrashFolder': 'Trash',
            'autoCheckInterval': '0',
            'accountReplyTo': '',
            'port': '993',
            'smtpUser': '',
            'accountOrder': '0',
            'accountName': 'accountname',
            'smtpHost': 'smtp.mail.yahoo.com',
            'imapDraftsFolder': 'Drafts',
            'keepExternalMessages': 'true',
            'smtpUseAuthentication': 'true',
            'accountEmail': 'new.swisscom@yahoo.com',
            'signatureId': '',
            'imapSentFolder': 'Sent',
            'securityType': 'SSL',
            'host': 'imap.mail.yahoo.com',
            'password': 'laszlo123',
            'sendFromMainAccount': 'true',
            'smtpPassword': '',
            'smtpSecurityType': 'SSL',
            'checkOnStartup': 'true',
            'smtpUseMainCredentials': 'false',
            'useAuthentication': 'false',
            'smtpPort': '465',
            'accountFromEmail': 'new.swisscom@yahoo.com'
        }
    },
    'method': 'mail.externalAccount.test'
}







EXTERNAL_ACCOUNT_LIST = {"method":"mail.externalAccount.list", "params":{}}
EXTERNAL_ACCOUNT_DEL = {"method":"mail.externalAccount.delete", "params":{"ids" : []}}
EXTERNAL_ACCOUNT_GET = {"method":"mail.externalAccount.get", "params":{"id" : ""}}
EXTERNAL_ACCOUNT_POPIMPORT = {"method":"mail.externalAccount.popImport", "params":{"accountId" : ""}}
EXTERNAL_ACCOUNT_STORECER = {"method":"mail.externalAccount.storeCertificate", "params":{}}
EXTERNAL_ACCOUNT_UPDATE = {"method":"mail.externalAccount.update", "params":{"object" : {"port" : "993", "accountFromName" : "account from name", "password" : "laszlo123", "smtpSecurityType" : "SSL", "sendFromMainAccount" : "true", "id" : "", "imapDraftsFolder" : "Drafts", "username" : "username", "imapTrashFolder" : "Trash", "smtpPassword" : "", "imapJunkFolder" : "Junk", "securityType" : "SSL", "imapSentFolder" : "Sent", "accountEmail" : "accoutn mail", "smtpPort" : "465", "protocol" : "imap", "host" : "imap.mail.yahoo.com", "accountOrder" : "0", "smtpHost" : "smtp.mail.yahoo.com", "autoCheckInterval" : "0", "useAuthentication" : "false","smtpUseAuthentication" : "true","accountFromEmail" : "new.swisscom@yahoo.com","accountName" : "account name","smtpUseMainCredentials" : "false","signatureId" : "","checkOnStartup" : "true","keepExternalMessages" : "true","smtpUser" : "","accountReplyTo" : ""}}}

ALIAS_ADD = {"method":"mail.alias.create", "params":{"object" : {"id" : "", "preferredName" : "", "name" : "", "notes" : ""}}}
ALIAS_LIST = {"method":"mail.alias.list", "params":{}}
ALIAS_DELETE = {"method":"mail.alias.delete", "params":{"ids" : []}}
ALIAS_GET = {"method":"mail.alias.get", "params":{"id" : ""}}
ALIAS_UPDATE = {"method":"mail.alias.update", "params":{"object" : {"id" : "", "preferredName" : "", "name" : "", "notes" : ""}}}

MAIL_AUTO_REPLY = {"method":"mail.vacationMessage.save", "params":{"object" : {}}}	
AUTO_REPLY_LOAD = {"method":"mail.vacationMessage.load", "params":{}}

IMAGE_BLOCKER_SAVE = '<request><imageBlocker action="save" value="%s" ></imageBlocker></request>'

#trust sender
TRUST_SENDER_CREATE = {"method":"mail.trustedSender.create", "params":{"object" : {}}}
TRUST_SENDER_DELETE = {"method":"mail.trustedSender.delete", "params":{"ids" : []}}
TRUST_SENDER_LIST = {"method":"mail.trustedSender.list", "params":{}}
TRUST_SENDER_GET = {"method":"mail.trustedSender.get", "params":{}}
TRUST_SENDER_UPDATE = {"method":"mail.trustedSender.update", "params":{"object" : {}}}
	
# Preference Service
#PROFILE_SETTING = '<request><prefs action="set"><prefs name="attr.user.FirstName">%s</prefs><prefs name="attr.user.LastName">%s</prefs><prefs name="attr.user.AlternateEmail"></request>'


TIMEZONE_LIST = {"method":"timezone.list", "params":{}}
TIMEZONE_SET = {"method":"timezone.set", "params":{"zoneId" : ""}}
'<request><timezone action="set" zoneId="%s" ></timezone></request>'
TIMEZONE_GET = '<request><timezone action="get" limit="25"></timezone></request>'

# config - bootstrap
BOOTSTRAP_GET_CONFIG = {"method" : "bootstrap.getConfig"}


# prefs
PREFS_SET = {"method" : "prefs.set", "params":{"map":{} } }
PREFS_GET = {"method" : "prefs.get", "params":{} }
PREFS_SET_GENERAL_PREFS = {"method" : "prefs.set", "params":{}, "id": "generalPreference"} 




# mail preference
SUB_MAIL_PREFERRENCE = '<mailpreference %s="%s" />'
MAIL_PREFERENCE_SAVE = {"method": "mail.preference.save",
						"params": {
							"object": {
								"id": 'null',
								"realName": 'null',
								"autoCheckInterval": 300,
								"from": 'null',
								"replyTo": 'null',
								"replyQuoting": 'null',
								"saveOutgoingMessages": 'true',
								"imageBlockerOption": "alwaysBlock",
								"preferPlaintext": 'false',
								"preferPlaintextEditor": 'null',
								"playSound": 'null',
								"autoInsertSignature": 'true',
								"spellcheckOnSend": 'null',
								"requestReceiptWithNewMail": 'false',
								"sendingReceipt": 2,
								"permanentDelete": 'null',
								"showCheckmarks": 'null',
								"accountName": 'null',
								"emptyTrashOnLogout": 'true',
								"maxMessagesPerFetch": 'null',
								"maxMessageSizePerFetch": 'null'
							}
						},
						"id": "mailpreference"}
MAIL_PREFERENCE_LOAD = {"method":"mail.preference.load", "params":{}}

#contact request
ADDRESSBOOK_LIST = {"method":"contacts.addressBook.list","params":{}}
ADDRESSBOOK_LIST_TYPES = {"method":"contacts.addressBook.listTypes","params":{}}
ADDRESSBOOK_CREATE = {'method':'contacts.addressBook.create','params':{'object':{"type" : "Webtop"}}}
ADDRESSBOOK_DEL = {'method':'contacts.addressBook.delete', 'params':{}}
ADDRESSBOOK_UPDATE = {'method':'contacts.addressBook.update','params':{'object':{"type" : "Webtop"}}}
ADDRESSBOOK_GET = {'method':'contacts.addressBook.get', 'params':{}}
ADDRESSBOOK_EMPTY_TRASH = {'method':'contacts.addressBook.emptyTrash'}

GROUP_CREATE = {'method':'contacts.createGroup', 'params':{'addressBookId':'', 'group':{'name' : '', '@type' : 'Group'}  }}
GROUP_LIST = '<request><contacts action="list" typeFilter="group" addressBookId="%s" offset="0" pageSize="300" limit="25"></contacts></request>'
GROUP_DEL = {'method':'contacts.deleteGroups', 'params':{'addressBookId':'', 'groupIds':[]}}
GROUP_GET = {'method':'contacts.getGroup', 'params':{'addressBookId':'', 'groupId':''}}
GROUP_RENAME = {'method':'contacts.renameGroup', 'params':{}}
GROUP_ADD_EMAL = {'method':'contacts.addGroupEmail', 'params':{}}

CONTACT_LIST = {'method':'contacts.list', 'params':{}}
CONTACT_LIST_ALL = {'method':'contacts.listAll', 'params':{}}
CONTACT_CREATE = {'method':'contacts.createContact','params':{'addressBookId':'', 'contact':{}, 'checkForDuplicates':'false'} }
CONTACT_GET = {'method':'contacts.getContacts','params':{}}
CONTACT_GET_INDEX = {'method':'contacts.getIndex', 'params':{'addressBookId':'',}}  # .../kiwi-octane/apidoc/#contacts.getIndex
CONTACT_FIELD = '<contactfield label="%s" type="%s" value="%s" primary="%s"/>'
CONTACT_DEL = {'method':'contacts.deleteContacts', 'params':{'addressBookId':'', 'contactIds':[]}}
CONTACT_UPDATE = {'method':'contacts.updateContact','params':{'addressBookId':'', 'contact':{}, 'checkForDuplicates':'false'} }
CONTACT_SETPHOTO = {'method':'contacts.setPhoto', 'params':{'addressBookId':'', 'contactId':'', 'photo':''}}

GROUPCONTACT_ADD = {'method':'contacts.addGroupContact', 'params':{} }
GROUPCONTACT_DEL = {'method':'contacts.deleteGroupContact','params':{} }

LIST_DUP = {'method':'contacts.listDuplicates', 'params':{'addressBookId':''}}
LIST_NEW_DUP = {'method':'contacts.listNewDuplicates', 'params':{'addressBookId':'', 'contactIds':[]}}
PREVIEW_MERGE = {'method':'contacts.previewMerge','params':{'addressBookId':'','contactIds':[]}}
MERGE_ALL_DUP = {'method':'contacts.mergeAllDuplicates','params':{}}

SUGGEST_REQUEST = {'method':'contacts.suggest', 'params':{'filter':''}}
COLLECTED_ADDRESS_COLLECT = {'method':'mail.collectedAddress.collect', 'params':{'addresses':[]} }
COLLECTED_ADDRESS_LIST = {'method':'mail.collectedAddress.list'}
COLLECTED_ADDRESS_DEL = {'method':'mail.collectedAddress.delete', 'params':{'ids':[]}}
COLLECTED_ADDRESS_GET = {'method':'mail.collectedAddress.get', 'params':{'id':''}}

IMPORT_CONTACT = {'method':'contacts.import', 'params':{'addressBookId':'', 'source':{}}}
CONTACT_AUTOSUGGEST = '<request><prefs action="set"><prefs name="contacts.autoSuggestCL">%s</prefs></prefs></request>'
CREATE_AUTOCOMPLETE_CONT = '<request><autocomplete action="create"><autocomplete address="%s"/></autocomplete></request>'
# COLLECT_AUTOCOMPLETE_CONT = '<request><autocomplete action="collect"><address>%s</address></autocomplete></request>'
DEL_AUTOCOMPLETE = '<request><autocomplete action="delete"><id>%s</id></autocomplete></request>'
DEL_AUTOCOMPLETE_CTNR = '<request><autocomplete action="delete">%s</autocomplete></request>'
DEL_AUTOCOMPLETE_NODE = '<id>%s</id>'
# createaContactRequest = '<request><contacts action="create_contact" addressBookId="%s" ><contact firstName="%s" lastName="%s" ></contact></contacts></request>'
CONTACT_GETINDEX = '<request><contacts-json action="getIndex">%s</contacts-json></request>'




#calendar request
CALENDAR_LIST = {'method':'calendar.list'}
CALENDAR_CREATE = {'method':'calendar.create', 'params':{'name':'','color':''}}
CALENDAR_DEL = {'method':'calendar.delete', 'params':{'id':''}}
CALENDAR_EMPTY = {'method':'calendar.empty', 'params':{'id':''}}
CALENDAR_RENAME = {'method':'calendar.rename', 'params':{'id':'','name':''}}
CALENDAR_SETCOLOR = {'method':'calendar.setColor', 'params':{'id':'','color':''}}
CALENDAR_SETVISIBLE = {'method':'calendar.setVisible', 'params':{'id':'','visible':True}}
CALENDAR_GET_ACCESSLIST = {'method':'calendar.getAccessList', 'params':{'calendarId':''}}
CALENDAR_SET_ACCESSLIST = {'method':'calendar.setAccessList', 'params':{'calendarId':'','ownerName':'','accessList':''}}
SUBSCRIBE_CALENDAR = {'method':'calendar.subscribe', 'params':{'url':''}}
LIST_SUBSCRIBED = {'method':'calendar.listSubscribed'}

CALENDAR_PREFERENCE_SAVE = {'method':'calendar.preference.save', 'params':{'prefs':{}}}
CALENDAR_PREFERENCE_LOAD = {'method':'calendar.preference.load'}

#event
EVENT_REPORT = {'method':'calendar.event.report', 'params':{'calendarIds':[], 'startTime':'', 'endTime':'' , 'filter' : {} }}
EVENT_READ = {'method':'calendar.event.read', 'params':{'calendarId':'', 'eventId':''}}
EVENT_DEL = {'method':'calendar.event.delete', 'params':{'calendarId':'', 'eventId':''}}
EVENT_CREATE = {'method':'calendar.event.create', 'params':{'event':'', 'attachments':[]}}
EVENT_UPDATE = {'method':'calendar.event.update', 'params':{'event':''}}
EVENT_SEND_INVITE = {'method':'calendar.event.sendInvite', 'params':{'event':'', 'notifyType':''}}
EVENT_COPY = {'method':'calendar.event.copy', 'params': {'calendarId':'', 'eventId':'', 'destCalendarId':''}}
EVENT_IMPORT={'method':'calendar.import', 'params':{'id':'',  'tasklist':'',  'resource':''}} # to be write
RSVP_UPDATE = {'method':'calendar.event.updateRsvp', 'params':{'status':'','ownerName':'','calendarId':'','ownerId':'','eventUid':'','email':''}} # status: ACCEPTED/DECLINED/TENTATIVE
#instance/all



EVENT_EXPORT='<resource resolver="calendar" calendarId="%s" filename="%s" componentType="%s"/>'


CALENAR_SHARE = '<calendar action="setAccessList" limit="25"><accessList calendarId="%s" ownerName="%s" ><users><user type="anyInternal" level="freebusy"/><user level="%s" username="%s"/></users></accessList></calendar>'

CALENDAR_SHARE_ALLOW_ANYONE = '<calendar action="setAccessList"><accessList calendarId="%s" ownerName="%s"><users><user type="anyInternal" level="freebusy"/><user type="anyone" level="read"/></users></accessList></calendar>'

SAVE_SHAREDCALENDAR = '<request><calendar action="saveSharedCalendar" calid="%s" ownername="%s" name="%s" ></calendar></request>'

# tasklist request
CREATE_TASKLIST = {'method':'calendar.taskList.create', 'params':{'taskList':''}}
LIST_TASKLIST = {'method':'calendar.taskList.list', 'params':{'calendarId':''}}
DEL_TASKLIST = {'method':'calendar.taskList.deleteTaskList', 'params':{'calendarId':'', 'taskListId':''}}
UPDATE_TASKLIST = {'method':'calendar.taskList.update', 'params':{'taskList':''}}
SHARE_TASKLIST_BY_MAIL = {'method':'calendar.taskList.shareTaskListByEmail', 'params':{'calendarId':'', 'taskListId':'', 'addresses':[]  }}
SHARE_TASK_BY_MAIL = {'method':'calendar.taskList.shareTaskByEmail', 'params':{'calendarId':'', 'taskIds':[], 'addresses':[] }}
# task request
TODO_REPORT = {'method':'calendar.toDo.report', 'params':{'calendarId':''}}   # calendarId, startTime, endTime, filter, page 
TODO_CREATE = {'method':'calendar.toDo.create', 'params':{'toDo':''}}
TODO_UPDATE = {'method':'calendar.toDo.update', 'params':{}}
DEL_TODO = {'method':'calendar.toDo.delete', 'params':{}}
TODO_MOVE = {'method':'calendar.toDo.move', 'params':{}}

ADVANCED_SEARCH = '''<request>
	<calendar action="%s" localStart="%sT000000" localEnd="%sT000000" categories="%s" alarmsOnly="%s" 
	includeMasterEvents="false" filter="%s" pageSize="20" offset="0">
	</calendar>
	</request>'''
 
 
# user
GET_CURRENT_USER_INFO = {"method":"user.getCurrentUserInfo"}
USER_CHANGE_PWD = {'method':'user.changePassword', 'params':{"newPassword" : "", "oldPassword" : "" }}
 
 
# resource_load - resource descriptors
RESOURCE_UPLOAD =  {'descriptor': {"@resolver": "Upload", "id": ""}} # UploadResourceDescriptor
RESOURCE_DOWNLOAD_EVENTS = {'descriptor': {'componentType': 'EVENT', 'calendarId': '', '@resolver': 'calendar', 'filename': ''} } # CalendarResourceDescriptor
RESOURCE_DOWNLOAD_CONTACTS = {'descriptor': {'addressBookId': '', '@resolver': 'contact', 'filename': '', 'format':''}} # ContactResourceDescriptor, format:outlook2010/vcard3 
RESOURCE_DOWNLOAD_CONTACT_PHOTO = {'descriptor': {'@resolver': 'ContactPhoto', 'contactId': '', 'addressBookId':'' }  } # ContactPhotoResourceDescriptor

RESOURCE_DOWNLOAD_MSG_VIEWSOURCE = {'descriptor': {'accountId': '', '@resolver': 'mail', 'folder': '', 'uid':''} }
 
# GET request url
SAVE_MAIL_TO_COMPUTER = '?r=resource.download{descriptor:{resolver:"mail",attributes:{accountId:"%s",folderPath:"%s",messageUid:%s}}}'
 
#temmplate
CONTACT_FIELD = '<contactfield value="%s" primary="false" type="%s" label="%s"/>'

#for signature delete all
SIGNATURE_DEL_CNTR = '<request><mailSignature action="delete">%s</mailSignature></request>'
SIGNATURE_ID_NODE = '<id>%s</id>'


'''
<request><mailForwarding action="save"><mailforwarding enabled="true" keepCopy="true" sendAsAttachment="false"><address email="webtopqa8@rwc-hinoki05.owmessaging.com"/></mailforwarding></mailForwarding></request>
'''

# GET request url
saveMailToComputer = '?r=resource.download{descriptor:{resolver:"mail",attributes:{accountId:"%s",folderPath:"%s",messageUid:%s}}}'

MAIL_AUTO_REPLY_CPMS = '''<request><mailVacationMessage action="save">
<vacationmessage enabled="%s" message="%s" startDate="%s" endDate="%s" replyOnce="%s" altDomains="%s" altMessage="%s" interval="%s" frequency="%s">
%s
</vacationmessage>
</mailVacationMessage>
</request>'''  # %s represent the whole option node
MAIL_AUTO_REPLY_DISABLE_CPMS = '<mailVacationMessage action="save"><vacationmessage enabled="false" message="" interval="0"><options><option name="onlyReplyToEnvelopeOriginator" value="false" /><option name="attachOriginalMessageToReply" value="false" /><option name="setReplyEnvelopeFromToRecipient" value="false" /><option name="vacationMode" value="false" /><option name="unconditionalReply" value="false" /></options></vacationmessage></mailVacationMessage>'

MOBILE_MAIL_PREFERENCE_SAVE = {"method":"mail.mobilePreference.save", "params":{"object" : {}}}
MOBILE_MAIL_PREFERENCE_LOAD = {"method":"mail.mobilePreference.load", "params":{}}

file_upload={"method":"fileUpload.upload", "params":{}}

UPLOAD_CLEARALL={"method":"fileUpload.clearAll", "params":{}}
UPLOAD_CLEARFILE={"method":"fileUpload.clearFile", "params":{}}
UPLOAD_GETCONFIG={"method":"fileUpload.getConfig", "params":{}}
UPLOAD_GET_PROGRESS={"method":"fileUpload.getProgress", "params":{}}
UPLOAD_PAUSE={"method":"fileUpload.pauseFile", "params":{}}
UPLOAD_PREPARE={"method":"fileUpload.prepareUpload", "params":{}}
UPLOAD_RESUME={"method":"fileUpload.resumeFile", "params":{}}
UPLOAD_SET_RATE={"method":"fileUpload.setRate", "params":{}}
# UPLOAD_UPLOAD={"method":"fileUpload.upload", "params":{}}
UPLOAD_UPLOAD={}
UPLOAD_VERIFY_CRC={"method":"fileUpload.verifyCrcOfUncheckedPart", "params":{}}









