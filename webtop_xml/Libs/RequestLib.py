import time, datetime, random

loginRequest = '<request><user action="login" username="%s" password="%s" rememberme="false"></user></request>'
logoutRequest = '<request><user action="logout"></user></request>'

# Mail
msgsendRequest = '<request><mail action="msgsend" accountId="" windowId="1" from="%s" to="%s" cc="%s" bcc="%s" subject="%s runtime" returnReceipt="false" rootMessageUID="null" priority="%s" bodytype="%s" limit="25"><body>automation test content</body></mail></request>'.replace('runtime',time.ctime())
msgheaderlist = '<request><mail action="msgheaderlist" accountId="" folder="%s" sortby="date" sortorder="desc" start="0"></mail></request>'
msgheaderlist_receipt = '<request><mail action="msgheaderlist" accountId="%s" folder="%s" sortby="date" sortorder="desc" start="0"></mail></request>'
msgheaderlistcheck = '<request><mail action="msgheaderlistcheck" accountId="" folder="%s" sortby="date" sortorder="desc" uidnext="%s"></mail></request>'
msgfetchRequest = '<request><mail action="msgfetch" accountId="" folder="%s" uid="%s" html="%s"></mail></request>'
msgmove = '<request><mail action="msgmove" uidnext="%s" folder="%s" accountId="" dstfolder="%s" uids="%s"></mail></request>'
msgflag = '<request><mail action="msgflag" accountId="" folder="%s" sortby="date" sortorder="desc" uidnext="%s" uids="%s" flag="%s" value="%s"></mail></request>'
msgreport = '<request><mail action="msgreport" type="junk" accountId="" sortby="date" dstfolder="%s" sortorder="desc" folder="%s" uids="%s"></mail></request>'
vmsgheaderlist = '<request><mail action="vmsgheaderlist" accountId="" folder="//\search//\" sortby="%s" sortorder="%s" count="100" pieces="%s" folders="%s" start="0" limit="100"></mail></request>'
vmsgheaderlist2 = '<request><mail action="vmsgheaderlist" accountId="" folder="//\search//\" sortby="date" sortorder="desc" start="0" count="25" text="%s" recursive="false" pieces="subject,from,recipients,body," folders="%s" recipients="1"></mail></request>'
msgdelete = '<request><mail action="msgdelete" accountId="" uidnext="%s" folder="Trash" sortby="date" sortorder="desc" uids="%s"></mail></request>'
msgheaderlist_sort='<request><mail action="msgheaderlist" accountId="" folder="%s" sortby="%s" sortorder="%s" count="100" start="0" limit="100"></mail></request>'

vmsgheaderlistadvanced='<request><mail action="vmsgheaderlistadvanced" accountId="" folder="//\search//\\" sortby="date" sortorder="desc" count="50" recipient="%s" sender="%s" subject="%s" body="%s" before="%s" after="%s" folders="%s" start="0" limit="50"></mail></request>'
msgsendRequest_search = '<request><mail action="msgsend" accountId="" windowId="1" from="%s" to="%s" cc="%s" bcc="%s" subject="%s" returnReceipt="false" rootMessageUID="null" priority="%s" bodytype="%s" limit="25"><body>%s</body></mail></request>'
msgsendRequest_receipt = '<request><mail action="msgsend" accountId="" windowId="1" from="%s" to="%s" cc="%s" bcc="%s" subject="%s" returnReceipt="%s" rootMessageUID="null" notifyOptions="%s" priority="%s" bodytype="%s" limit="25"><body>%s</body></mail></request>'
msgSendReceipt = '<request><mail action="sendreceipt" uid="%s" accountId="" folder="INBOX"></mail></request>'
msgIgnoreReceipt = '<request><mail action="ignorereceipt" uid="%s" accountId="" folder="INBOX"></mail></request>'

foldercreatereq = '<request><mail action="foldercreate" name="%s" parent="%s" accountId=""></mail></request>'
folderlistRequest = '<request><mail action="folderlist" accountId="%s" folder="%s" depth="-1"></mail></request>'
foldermove = '<request><mail action="foldermove" accountId="" source="%s" target="%s" limit="25"></mail></request>'
folderrename = '<request><mail action="folderrename" accountId="" source="%s" target="%s"></mail></request>'
folderdelete = '<request><mail action="folderdelete" accountId="" name="%s"></mail></request>'
folderempty = '<request><mail action="folderempty" name="%s" accountId=""></mail></request>'

# Mail Related
blockedsenderList = '<request><blockedsender action="load" limit="300"></blockedsender></request>'
blockedsenderModify = '<request><blockedsender action="modify"><add>%s</add></blockedsender></request>'
blocksender_remove = '<request><blockedsender action="modify">%s</blockedsender></request>'
safesender_add = '<request><allowedsender action="modify"><add>%s</add></allowedsender></request>'
sefesenderList = '<request><allowedsender action="load" limit="300"></allowedsender></request>'
safesender_remove = '<request><allowedsender action="modify">%s</allowedsender></request>'

mailSignature = '<mailSignature action="create" limit="25"><mailsignature id="" text="%s" label="%s" contentType="%s" isDefault="%s"/></mailSignature>'
signaturePosition = '<request><prefs action="set"><prefs name="attr.mail.signaturePosition">%s</prefs></prefs></request>'
mailSignatureList = '<request><mailSignature action="list" limit="25"></mailSignature></request>'
mailSignatureDelete = '<request><mailSignature action="delete" id="%s"></mailSignature></request>'
mailForwarding = '<request><mailForwarding action="save"><mailforwarding enabled="%s" keepCopy="%s" sendAsAttachment="%s"><address email="%s"/></mailforwarding></mailForwarding></request>'
mailpwdchange = '<request><user action="changePassword" oldPassword="%s" newPassword="%s"></user></request>'

prefsSet_template = '<request><prefs action="set"></prefs></request>'
prefsSet_mail = '''<request>
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
externalmailaccount = '<mailExternalAccount action="create"><externalmailaccount id="" password="laszlo123" username="new.swisscom@yahoo.com" host="imap.mail.yahoo.com" port="993" protocol="imap" useAuthentication="false" accountName="new.swisscom@yahoo.com" accountEmail="new.swisscom@yahoo.com" securityType="SSL" keepExternalMessages="true" checkOnStartup="true" autoCheckInterval="0" accountOrder="0" smtpUseAuthentication="true" smtpHost="smtp.mail.yahoo.com" smtpPort="465" smtpUseMainCredentials="false" smtpUser="" smtpSecurityType="SSL" smtpPassword="" sendFromMainAccount="true" imapSentFolder="Sent" imapDraftsFolder="Drafts" imapTrashFolder="Trash" imapJunkFolder="Junk" accountReplyTo="" accountFromName="new.swisscom@yahoo.com" accountFromEmail="" signatureId=""/></mailExternalAccount>'

externalmailaccount_test = '<mail action="testexternalaccountconnection"><externalmailaccount id="" password="laszlo123" username="new.swisscom@yahoo.com" host="imap.mail.yahoo.com" port="993" protocol="imap" useAuthentication="false" accountName="new.swisscom@yahoo.com" accountEmail="new.swisscom@yahoo.com" securityType="SSL" keepExternalMessages="true" checkOnStartup="true" autoCheckInterval="0" accountOrder="0" smtpUseAuthentication="true" smtpHost="smtp.mail.yahoo.com " smtpPort="465" smtpUseMainCredentials="false" smtpUser="" smtpSecurityType="SSL" smtpPassword="" sendFromMainAccount="true" imapSentFolder="Sent" imapDraftsFolder="Drafts" imapTrashFolder="Trash" imapJunkFolder="Junk" accountReplyTo="" accountFromName="new.swisscom@yahoo.com" accountFromEmail="" signatureId=""/></mail>'

externalAccountList = '<request><mailExternalAccount action="list" limit="25"></mailExternalAccount></request>'
mailExternalAccountDel = '<mailExternalAccount action="delete" id="%s"></mailExternalAccount>'
saveOutgoingMessages = '''<request>
				<mailPreference action="save">
				<mailpreference saveOutgoingMessages="%s" autoCheckInterval="%s" replyQuoting="%s"/>
				</mailPreference>
				</request>'''
trustedsender = '<request><trustedsender action="list" limit="25"></trustedsender></request>'
mailAlias_add = '<mailAlias action="create" accountName="DefaultMailAccount" limit="300"><mailalias id="" name="%s" mailAddress=""\
 accountName="DefaultMailAccount" preferredName="%s" notes="some test notes"/></mailAlias>'
mailAlias_list = '<request><mailAlias action="list" accountName="DefaultMailAccount" limit="300"></mailAlias></request>'
mailAlias_delete = '<request><mailAlias action="delete" id="%s"></mailAlias></request>'
autoReply =	'''	<request><mailVacationMessage action="save">
		<vacationmessage enabled="true" message="this is %s auto reply msg~" altDomains="%s" altMessage="%s">
		<startDate/>
		<endDate/>
		<options/>
		</vacationmessage></mailVacationMessage></request>'''
autoReply_load = '<request><mailVacationMessage action="load" limit="25"></mailVacationMessage></request>'
imageBlocker = '<request><imageBlocker action="save" value="%s"></imageBlocker></request>'	
trustImgSender = '<trustedsender action="create" limit="300"><trustedsender address="%s" id=""/></trustedsender>'
imgTrustList = '<request><trustedsender action="list" limit="300"></trustedsender></request>'
imgtrustSender_delete = '<request><trustedsender action="delete">%s</trustedsender></request>'
	
# Preference Service	
profileSettings = '''<request>
		<prefs action="set">
		<prefs name="attr.user.FirstName">%s</prefs>
		<prefs name="attr.user.LastName">%s</prefs>
		<prefs name="attr.user.AlternateEmail">%s</prefs>
		<prefs name="attr.user.Mobile">%s</prefs>
		</prefs>
		<mailPreference action="save">
		<mailpreference realName="%s"/>
		</mailPreference>
		</request>'''
timezonelist = '<request><timezone action="list"></timezone></request>'
timezoneSet = '<request><timezone action="set" zoneId="%s"></timezone></request>'
timezoneGet = '<request><timezone action="get" limit="25"></timezone></request>'
singlePrefSet = '<request><prefs action="set"><prefs name="attr.user.%s">%s</prefs></prefs></request>'  
prefsGet = '<request><prefs action="get" limit="25"></prefs></request>'

#contact request
listAddressBookRequest = '<request><addressbooks action="list" limit="25"></addressbooks></request>'
createAddressBook = '<addressbooks action="create" limit="25"><addressbook id="" name="%s" type="Webtop"/></addressbooks>'
deleteAddressBook = '<request><addressbooks action="delete" id="%s"></addressbooks></request>'
createGroup = '<contacts action="create_group" typeFilter="group" pageSize="300" addressBookId="%s"><contactgroup id="" type="group" name="%s" size=""/></contacts>'
listGroup = '<request><contacts action="list" typeFilter="group" addressBookId="%s" offset="0" pageSize="300" limit="25"></contacts></request>'
deleteGroup = '<request><contacts action="delete_group" addressBookId="%s" group_id="%s"></contacts></request>'
getGroup = '<request><contacts action="get_group" addressBookId="%s" group_id="%s" limit="25"></contacts></request>'
listContacts = '<request><contacts action="list" pageSize="300" addressBookId="%s" offset="0" typeFilter="contact"></contacts></request>'
createContact = '<contacts action="create_contact" addressBookId="%s"><contact id="" firstName="%s" lastName="%s" type="contact" name="%s"></contact></contacts>'
deleteContact = '<request><contacts action="delete_contact" addressBookId="%s"></contacts></request>'
addGroupContact = '<request><contacts action="add_group_contact" addressBookId="%s" group_id="%s"></contacts></request>' # add a contact from addressbook to group
listdup = '<request><contacts action="list_duplicates" addressBookId="%s" limit="25"></contacts></request>'
getContactsInfo = '<request><contacts action="get_contacts" addressBookId="%s" limit="25"></contacts></request>'
previewMerge = '<request><contacts action="preview_merge" addressBookId="%s" limit="25">%s</contacts></request>'
updateContact = '<contacts action="update_contact" addressBookId="%s"><contact id="%s" firstName="%s" lastName="%s" type="contact" name="%s">fieldbody</contact></contacts>'
autoSuggestCL = '<request><prefs action="set"><prefs name="contacts.autoSuggestCL">%s</prefs></prefs></request>'
# createAutocompleteCont = '<request><autocomplete action="create"><autocomplete address="%s"/></autocomplete></request>'
createAutocompleteCont = '<request><autocomplete action="collect"><address>%s</address></autocomplete></request>'
suggestRequest = '<request><contacts action="suggest" filter="%s" limit="25" requiredField="lzEmail"></contacts></request>'
listAutocomplete = '<request><autocomplete action="list" limit="25"></autocomplete></request>'
deleteAutocomplete = '<request><autocomplete action="delete">%s</autocomplete></request>'
# createaContactRequest = '<request><contacts action="create_contact" addressBookId="%s"><contact firstName="%s" lastName="%s"></contact></contacts></request>'
contactfield = '<contactfield type="%s" label="%s" value="%s" primary="%s" /></contact>'
importContact = '<request><contacts action="import" addressBookId="%s" fileid="%s"></contacts></request>'

#calendar request
calendarCreate = '<calendar action="createCalendar" timezone="" limit="25"><calendar id="" url="" name="%s" color="%s" shown="false" readOnly="false" published="false" primary="false" personal="true"/></calendar>' 
listCalendars = '<request><calendar action="listCalendars" timezone="" limit="25"></calendar></request>'
deleteCalendar = '<calendar action="deleteCalendar" timezone="" limit="25"><calendar id="%s" url="%s" name="%s" color="" shown="true" readOnly="false" published="true" primary="false" personal="true"/></calendar>'
updateCalendar = '<calendar action="updateCalendar" timezone="" limit="25"><calendar id="%s" url="%s" name="%s" color="%s" shown="true" readOnly="false" published="true" primary="false" personal="true"/></calendar>'
createEvent = '''<calendar action="createEvent" timezone="" affects="instance">
		 <event id="" summary="%s" location="%s" url="" etag="" startTime="" endTime="" localStart="%s" allDay="%s" 
		 floating="false" busyStatus="BUSY" class="PUBLIC" notificationEmailTimeDiff="0" notificationMobileTimeDiff="0" recurrenceOf="" 
		 calendarId="%s"  localEnd="%s">
		 <description>%s</description>
		 <tag></tag>
		 <categories>%s</categories>
		 </event>
		 </calendar>'''
reportEvents = '''<request>
	<calendar action="reportEvents" eventLimit="1000" timezone="" localStart="%sT000000" localEnd="%sT235959" limit="25">
	</calendar>
	</request>'''
deleteEvent = '''<calendar action="deleteEvent" calendarId="%s" id="%s" notifyType="CANCEL_EVENT" affects="%s">%s</calendar>'''
updateRsvpReq = '<request><calendar action="updateRsvp" opt="%s" calid="%s" ownerid="%s" ownername="%s" eid="%s" email="%s"></calendar></request>'
importEventTask = '<request><calendar action="import" calendarId="%s" fileid="%s"></calendar></request>'
readEvent = '<request><calendar action="readEvent" calendarId="%s" id="%s" timezone="" affects="instance"></calendar></request>'
shareCalenar = '<calendar action="setAccessList" limit="25"><accessList calendarId="%s" ownerName="%s"><users><user type="anyInternal" level="freebusy"/><user level="%s" username="%s"/></users></accessList></calendar>'
saveSharedCalendar = '<request><calendar action="saveSharedCalendar" calid="%s" ownername="%s" name="%s"></calendar></request>'
subscribeCalendar = '<calendar action="subscribeCalendar"><calendar id="" url="%s" name="%s" color="5" shown="false" readOnly="false" published="false" primary="false" personal="true"/></calendar>'

#task request
createTaskGroup = '<calendar action="createTaskList" calendarId="%s" limit="25"><tasklist calendarId="%s" id="" name="%s"/></calendar>'
listTaskLists = '<request><calendar action="listTaskLists" calendarId="%s" limit="25"></calendar></request>'
updateTaskList = '<calendar action="updateTaskList" calendarId="%s" limit=""><tasklist calendarId="%s" id="%s" name="%s"/></calendar>'
deleteTaskList = '<calendar action="deleteTaskList" calendarId="%s" limit="">%s</calendar>'
createTask = '''<calendar action="createToDo" calendarId="%s" limit="25">
		<todo id="%s" calendarId="%s" summary="%s" priority="%s" status="%s" dueTime="0" localDue="%s" url="%s">
		<xproperty name="X-CP-TASKLIST" value="%s"/>
		<description>%s</description>
		</todo>
		</calendar>'''
reportToDos = '<request><calendar action="reportToDos" calendarId="%s" limit=""></calendar></request>'
deleteToDo = '''<calendar action="deleteToDo" calendarId="%s" limit="">%s</calendar>'''
advancedSearch = '''<request>
	<calendar action="%s" localStart="%sT000000" localEnd="%sT000000" categories="%s" alarmsOnly="%s" 
	includeMasterEvents="false" filter="%s" pageSize="20" offset="0">
	</calendar>
	</request>'''
 
 
# GET request url
saveMailToComputer = '?r=resource.download{descriptor:{resolver:"mail",attributes:{accountId:"%s",folderPath:"%s",messageUid:%s}}}'
 
#temmplate
contactField = '<contactfield value="%s" primary="false" type="%s" label="%s"/>'

#for signature delete all
signature_delete_cntr = '<request><mailSignature action="delete">%s</mailSignature></request>'
signature_id_node = '<id>%s</id>'


mail_empty_trash_logout = '<request><mailPreference action="save"><mailpreference emptyTrashOnLogout="%s" /></mailPreference></request>'

#mail_list_all_attachment = '<mail action="vmsgheaderlistattachments" folder="%s" count="20" sortby="natural" sortorder="desc"/>'
#mail_list_attachment_more = '<mail action="vmsgheaderlist" vfolder="%s" start="20" count="20" sortby="natural" sortorder="desc"/>'




