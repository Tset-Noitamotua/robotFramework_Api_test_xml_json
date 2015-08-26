#attention: avoid user " in default parameters
import time, datetime, random
now = datetime.datetime.now()
#log
LOGIN={'rememberme' : 'false'}
LOGOUT={}
#mail
#foldername, answered,rootMessageUID is used for reply a mail?
MSG_SEND={
'from' : 'test@rwc-hinoki03.owmessaging.com',
'to'   : 'test@rwc-hinoki03.owmessaging.com',
'subject':'mail subject',
'priority' : '3',
'bodytype' : 'plain',
'limit' : '25',
'body' : 'text body',
'returnReceipt' : 'false',
'notifyOptions' : '',
'rootMessageUID' : 'null',
'answered' : '',
'forwarded' : '',
'foldername' : ''}#NEVER, SUCCESS, FAILURE, DELAY
MSG_HEADER_LST={ 
'folder' : 'INBOX', 
'sortorder' : 'desc',
'sortby' : 'date',
'start' : '0',
'couont' : '100',
'limit' : '100'}
VMSG_HEADER_LST={'sortby' : 'date',
'sortorder' : 'desc',
'count' : '50',
'text' : 'test',
'pieces' : 'recipients,from,subject,body,',
'start' : '0',
'limit' : '50',
'folder' : 'INBOX'
}
MSG_HEADER_LST_CHECK={
'sortby' : 'date' ,
'sortorder' : 'desc'
}
MSG_FLAG={
'sortby' : 'date',
'sortorder' : 'desc',
'flag' : 'seen',
'value' : '1',
'folder' : 'INBOX'}
MSG_REPORT={
'sortby' : 'date',
'sortorder' : 'desc',
'type' : 'junk'}
VMSG_HEADER_LST_ADVANCED={
'sortby' : 'date',
'sortorder' : 'desc',
'count' : '50',
'folders' : '',
'start' : '0',
'limit' : '50'}
CALENDAR_CREATE={
'shown' : 'false',
'readOnly' : 'false',
'published' : 'false',
'primary' : 'false',
'personal' : 'true',
'color' : '9'
}
CALENDAR_UPDATE={
'shown' : 'false',
'readOnly' : 'false',
'published' : 'false',
'primary' : 'false',
'personal' : 'true'
}
MSG_FETCH={
'html' : 'text'
}
MSG_SAVE_DRAFT={
'from' : 'webtopqa7@rwc-hinoki05.owmessaging.com',
'to' : 'webtopqa6@rwc-hinoki05.owmessaging.com',
'subject' : 'draft mail',
'bodytype' : 'plain',
'limit' : '25'
}
FOLDER_EMPTY={}
MSG_MOVE={}
MSG_DEL={}
FOLDER_LIST={'depth' : '-1'}
FOLDER_CREATE={}
FOLDER_RENAME={}
FOLDER_MOVE={}
FOLDER_DELETE={}

SUB_PREF = {
'attr.user.mail.SendFormat' : 'plain',
'attr.user.mail.AutoSaveDraftFlag' : 'false',
'attr.user.mail.SaveToDraftsInterval' : '60',
'attr.user.mail.ReplyPrefix' : '-',
'autoCreateContact' : 'false',
'attr.user.mail.disableReloadOnDelete' : 'false',
'attr.user.mail.readFirstMail' : '',
'attr.user.mail.ViewMode' : '',
'attr.user.mail.IsConversation' : '',
'attr.user.mail.TimeDisplayFormat' : 'short',
}

PREFS_GET={}
SAVE_OUTGOING_MSG={
'saveOutgoingMessages' : 'false',
'autoCheckInterval' : '0',
'replyQuoting' : 'false'
}
EXTERNAL_ACCOUNT_DEL={}
EXTERNAL_ACCOUNT_LIST={'limit' : '25'}
EXTERNAL_MAIL_ACCOUNT_TEST={
'password' : 'laszlo123',
'accountName' : 'account_name',
'host' : 'imap.mail.yahoo.com',
'port' : '993',
'protocol' : 'imap',
'useAuthentication' : 'false',
'username' : 'new.swisscom@yahoo.com',#both fusion and kpn use this to test connection
'accountEmail' : 'account email',#useless
'securityType' : 'SSL',
'keepExternalMessages' : 'true',
'checkOnStartup' : 'true',
'autoCheckInterval' : '0',
'accountOrder' : '0',
'smtpUseAuthentication' : 'true',
'smtpHost' : 'smtp.mail.yahoo.com',
'smtpPort' : '465',
'smtpUseMainCredentials' : 'false',
'smtpUser' : '',
'smtpSecurityType' : 'SSL',
'smtpPassword' : '',
'sendFromMainAccount' : 'true',
'imapSentFolder' : 'Sent',
'imapDraftsFolder' : 'Drafts',
'imapTrashFolder' : 'Trash',
'imapJunkFolder' : 'Junk',
'accountReplyTo' : '',
'accountFromName' : 'account from name',
'accountFromEmail' : 'account from email',
'signatureId' : ''
}
EXTERNAL_MAIL_ACCOUNT={
'password' : 'laszlo123',
'accountName' : 'account name',
'host' : 'imap.mail.yahoo.com',
'port' : '993',
'protocol' : 'imap',
'useAuthentication' : 'false',
'username' : 'username',#fusion use this for connection
'accountEmail' : 'accoutn mail',#kpn check this field if accountFromEmail is not emial
'securityType' : 'SSL',
'keepExternalMessages' : 'true',
'checkOnStartup' : 'true',
'autoCheckInterval' : '0',
'accountOrder' : '0',
'smtpUseAuthentication' : 'true',
'smtpHost' : 'smtp.mail.yahoo.com',
'smtpPort' : '465',
'smtpUseMainCredentials' : 'false',
'smtpUser' : '',
'smtpSecurityType' : 'SSL',
'smtpPassword' : '',
'sendFromMainAccount' : 'true',
'imapSentFolder' : 'Sent',
'imapDraftsFolder' : 'Drafts',
'imapTrashFolder' : 'Trash',
'imapJunkFolder' : 'Junk',
'accountReplyTo' : '',
'accountFromName' : 'account from name',
'accountFromEmail' : 'new.swisscom@yahoo.com',#kpn check this field for create external account.but actually when list folder it use username for connection
'signatureId' : ''
}
EXTERNAL_MAIL_ACCOUNT_UPDATE={#same with EXTERNAL_MAIL_ACCOUNT(create external account)
'password' : 'laszlo123',
'accountName' : 'account name',
'host' : 'imap.mail.yahoo.com',
'port' : '993',
'protocol' : 'imap',
'useAuthentication' : 'false',
'username' : 'username',#fusion use this for connection
'accountEmail' : 'accoutn mail',#kpn check this field if accountFromEmail is not emial
'securityType' : 'SSL',
'keepExternalMessages' : 'true',
'checkOnStartup' : 'true',
'autoCheckInterval' : '0',
'accountOrder' : '0',
'smtpUseAuthentication' : 'true',
'smtpHost' : 'smtp.mail.yahoo.com',
'smtpPort' : '465',
'smtpUseMainCredentials' : 'false',
'smtpUser' : '',
'smtpSecurityType' : 'SSL',
'smtpPassword' : '',
'sendFromMainAccount' : 'true',
'imapSentFolder' : 'Sent',
'imapDraftsFolder' : 'Drafts',
'imapTrashFolder' : 'Trash',
'imapJunkFolder' : 'Junk',
'accountReplyTo' : '',
'accountFromName' : 'account from name',
'accountFromEmail' : 'new.swisscom@yahoo.com',#kpn check this field for create external account.but actually when list folder it use username for connection
'signatureId' : ''
}
SIGNATURE_CREATE={
'text' : 'this is my plain signaure',
'label' : 'this is my plain signaure label',
'contentType' : 'text/plain',
'isDefault' : 'false'
}
SIGNATURE_LIST={}
SIGNATURE_DEL={}
BLOCKED_SENDER_ADD={}
BLOCKED_SENDER_LIST={}
BLOCK_SENDER_REMOVE={}

SAFE_SENDER_LIST={}
SAFE_SENDER_REMOVE={}
SAFE_SENDER_ADD={}
MAIL_FORWARDING={
'keepCopy' : 'false',
'enabled' : 'true',
'sendAsAttachment' : 'false'
}
IMAGE_BLOCKER_SAVE={}
TRUST_IMG_SENDER_CREATE={}
ALIAS_ADD={
'name' : 'test-name@openwave.com',
'preferredName' : 'fake-name',
'notes' : 'test notes'
}
ALIAS_LIST={}
SEND_RECEIPT={}
IGNORE_RECEIPT={}
PREFS_EMPTY_TRASH_WHEN_LOGOUT={}
SUB_MAIL_PREFERRENCE={ # a lot of config didn't appear in UI settings
'saveOutgoingMessages' : 'false',
'autoCheckInterval' : '300',
'replyQuoting' : 'false',
'blockExternalImages' : 'false' ,
'preferPlaintext' : 'false' ,
'preferPlaintextEditor' : 'false' ,
'playSound' : 'false' ,
'autoInsertSignature' : 'false' ,
'spellcheckOnSend' : 'false' ,
'requestReceiptWithNewMail' : 'false' ,
'sendingReceipt' : '2' ,
'permanentDelete' : 'false' ,
'showCheckmarks' : 'false' ,
'emptyTrashOnLogout' : 'false' ,
'realName' : '' ,
'replyTo' : ''
}
USER_CHANGE_PWD={}
IMG_TRUST_LIST={}
MAIL_AUTO_REPLY = {
'enabled' : 'true' , 
'message' : 'This is auto-reply msg for MX backend',
'mode' : 'VACATION'#NONE, ECHO, REPLY, VACATION
}
MAIL_AUTO_REPLY_CPMS = {
'enabled' : 'true',
'message' : 'this is auto-reply msg for CMPS backend' ,
'startDate' : str(int(time.time())*1000) ,
'endDate' : str((int(time.time()) + 3600*24*2)*1000)
#'endDate' : str(int(time.mktime(datetime.datetime.strptime(now.replace(day=now.day+2).strftime('%Y%m%dT000'), '%Y%m%dT000').timetuple())*1000))
}
AUTO_REPLY_LOAD = {
'limit' : '25'
}
MAIL_AUTO_REPLY_DISABLE_CPMS = {}
#default paramater for calendar settings
CAL_PREFS_DEFAULT_VALUE ={
'calendar.defaultview' : ['Day', 'Week', 'Month', 'List'],
'attr.user.StartTimeOfDay' : range(0, 24),
'attr.user.endTimeOfDay' : range(0, 24),
'calendar.weekstart' : range(1, 8),
'calendar.timeinterval' : [0, 1, 10000],
'attr.user.CalendarReminderUnit' : ['minute', 'hour', 'day'],
'attr.user.TaskViewType' : ['taskgroup', 'single'],
'attr.user.TaskSortType' : ['priority', 'duedate', 'needaction', 'incomplete', 'complete', 'title'],
'attr.user.TaskReminderUnit' : ['minute', 'hour', 'day']
}

TIMEZONE_SET={}
TIMEZONE_LIST={
'query' : ''
}



#contact
CONTACT_LIST={
'filter' : '',
'sort' : 'lastName ASC'
}
SET_PHOTO={
'addressBookId' : '',
'contact_id' : '',
'id' :''
}
GET_CONTACT = {}
MOVE_CONTACT={}
ADDRESSBOOK_LIST={}
ADDRESSBOOK_CREATE={'name' : 'my address book'}
ADDRESSBOOK_DEL={}
ADDRESSBOOK_UPDATE={
'name' : 'update name',
'type' : 'Webtop'
}

GROUP_CREATE={}
GROUP_LIST={}
GROUP_DEL={}
GROUP_RENAME={}
GROUP_GET={}

CONTACT_CREATE={
'firstName' : 'first',
'lastName' : 'last',
'type' : 'contact',
'name' : '',
'check_dup' : 'false',
'contactFields' : [
{
'label' : 'middlename',
'type' : 'lzHeader',
'value' : 'middle',
'primary' : 'false'
},
{
'label' : 'nickname',
'type' : 'lzHeader',
'value' : 'nick',
'primary' : 'false'
},
{
'label' : 'home',
'type' : 'lzEmail',
'value' : 'home@openwave.com',
'primary' : 'false'
},
{
'label' : 'work',
'type' : 'lzEmail',
'value' : 'work@openwave.com',
'primary' : 'true'
},
{
'label' : 'other',
'type' : 'lzEmail',
'value' : 'other@openwave.com',
'primary' : 'false'
},
{
'label' : 'home',
'type' : 'lzPhone_mobile',
'value' : '12345678990',
'primary' : 'false'
},
{
'label' : 'work',
'type' : 'lzPhone',
'value' : '11100000',
'primary' : 'false'
},
{
'label' : 'street',
'type' : 'lzAddress_home',
'value' : 'street',
'primary' : 'false'
},
{
'label' : 'street2',
'type' : 'lzAddress_home',
'value' : 'street2',
'primary' : 'false'
},
{
'label' : 'street3',
'type' : 'lzAddress_home',
'value' : 'street3',
'primary' : 'false'
},
{
'label' : 'city',
'type' : 'lzAddress_home',
'value' : 'beijing',
'primary' : 'false'
},
{
'label' : 'state',
'type' : 'lzAddress_home',
'value' : 'haidian',
'primary' : 'false'
},
{
'label' : 'zip',
'type' : 'lzAddress_home',
'value' : '100091',
'primary' : 'false'
},
{
'label' : 'country',
'type' : 'lzAddress_home',
'value' : 'china',
'primary' : 'false'
},
{
'label' : 'birthday',
'type' : 'lzPersonal',
'value' : '19901010',
'primary' : 'false'
}
]
}
CONTACT_DEL={}
GROUPCONTACT_ADD={}
GROUPCONTACT_DEL={}
SUGGEST_REQUEST={
'limit' : '25',
'requiredField' : 'lzEmail'
}

CREATE_AUTOCOMPLETE_CONT={}
LIST_AUTOCOMPLETE={}
COLLECT_AUTOCOMPLETE_CONT={}
LIST_DUP={}
IMPORT_CONTACT={}

CALENDAR_LIST={
'timezone' : 'Asia/Chongqing',
'limit' : '25'
}

CALENDAR_DEL={}
EVENT_CREATE={
'summary' : 'default event name',
'location' : 'default location',
'startTime' : int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple())),
'endTime' : int(time.mktime(datetime.datetime.strptime('20190930T100000', '%Y%m%dT%H%M%S').timetuple())),
'allDay' : 'false',
'floating' : 'false',
'busyStatus' : 'BUSY',
'class' : 'PUBLIC',
'notificationEmailTimeDiff' : '0',#useless?
'notificationMobileTimeDiff' : '0',#useless?
'recurrenceOf' : '',#useless?
'localStart' : '',#useless?
'localEnd' : '',#useless?
'description' : 'default description',
'categories' : 'DOCTOR',#general = ''
#attendee--may be more than one attendee
#alarm
'triggered' : '0',
'trigger' : 'start',
'triggerOffset' : '-20',
'action' : 'email',
'address' : 'webtopqa6@openwave.com',
#organizer
'name' : 'webtopqa6',
'email' : 'webtopqa6@openwave.com',
'status' : 'NEEDS_ACTION',
'type' : 'INTERNAL',
#recurrence--different recurrence type has different field value
'freq' : 'daily',
'count' : '-1',
'interval' : '1',
'setPos' : '',
'monthDayList' : '',
'localUntil' : '20191130T235959',
'dayList' : ''
}
EVENT_CREATE_ATTENDEE={
#attendee--create event,update event, there may be more than one attendee
'email' : 'default@openwave.com',
'status' : 'NEEDS_ACTION',
'type' : 'INTERNAL'
}
import time, datetime
EVENT_REPORT={
'eventLimit' : '10000',
'startTime' : int(time.mktime(datetime.datetime.strptime('20180930T013000', '%Y%m%dT%H%M%S').timetuple())),
'endTime' : int(time.mktime(datetime.datetime.strptime('20201130T235959', '%Y%m%dT%H%M%S').timetuple())),
'includeMasterEvents' : 'false',
'pageSize' : '10000',
'offset' : '0',
'alarmsOnly' : 'false',
'categories' : '',
'filter' : ''
}

EVENT_DEL={
'affects' : 'instance'
}

#same params with EVENT CREATE
EVENT_SEND_INVITE={
'summary' : 'default event name',
'location' : 'default location',
'startTime' : int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple())),
'endTime' : int(time.mktime(datetime.datetime.strptime('20190930T100000', '%Y%m%dT%H%M%S').timetuple())),
'allDay' : 'false',
'floating' : 'false',
'busyStatus' : 'BUSY',
'class' : 'PUBLIC',
'notificationEmailTimeDiff' : '0',#useless?
'notificationMobileTimeDiff' : '0',#useless?
'recurrenceOf' : '',#useless?
'localStart' : '',#useless?
'localEnd' : '',#useless?
'description' : 'default description',
'categories' : 'DOCTOR',#general = ''
#attendee--may be more than one attendee
#alarm
'triggered' : '0',
'trigger' : 'start',
'triggerOffset' : '-20',
'action' : 'email',
'address' : 'webtopqa6@openwave.com',
#organizer
'name' : 'webtopqa6',
'email' : 'webtopqa6@openwave.com',
'status' : 'NEEDS_ACTION',
'type' : 'INTERNAL',
#recurrence--different recurrence type has different field value
'freq' : 'daily',
'count' : '-1',
'interval' : '1',
'setPos' : '',
'monthDayList' : '',
'localUntil' : '20191130T235959',
'dayList' : ''
}

RSVP_UPDATE={}
EVENT_UPDATE={
'affects' : 'instance',
'summary' : 'default event name',
'location' : 'default location',
'startTime' : int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple())),
'endTime' : int(time.mktime(datetime.datetime.strptime('20190930T100000', '%Y%m%dT%H%M%S').timetuple())),
'allDay' : 'false',
'floating' : 'false',
'busyStatus' : 'BUSY',
'class' : 'PUBLIC',
'notificationEmailTimeDiff' : '0',#useless?
'notificationMobileTimeDiff' : '0',#useless?
'recurrenceOf' : '',#useless?
'localStart' : '',#useless?
'localEnd' : '',#useless?
'description' : 'deault description',
'categories' : 'DOCTOR',#general = ''
#attendee--may be more than one attendee
#alarm
'triggered' : '0',
'trigger' : 'start',
'triggerOffset' : '-20',
'action' : 'email',
'address' : 'webtopqa6@openwave.com',
#organizer
'name' : 'webtopqa6',
'email' : 'webtopqa6@openwave.com',
'status' : 'NEEDS_ACTION',
'type' : 'INTERNAL',
#recurrence--different recurrence type has different field value
'freq' : 'daily',
'count' : '-1',
'interval' : '-1',
'setPos' : '',
'monthDayList' : '',
'localUntil' : '20191130T235959',
'dayList' : ''
}

EVENT_EXPORT={
'filename' : 'events.ics',
'componentType' : 'EVENT'
}
EVENT_IMPORT={}
CALENAR_SHARE={}
CALENDAR_SHARE_ALLOW_ANYONE={}
SUBSCRIBE_CALENDAR={
'name' : 'shared cal',
'color' : '5',
'shown' : 'false',
'readOnly' : 'false',
'published' : 'false',
'primary' : 'false',
'personal' : 'true'
}

CREATE_TASK={
'status' : 'IN-PROCESS',#IN-PROCESS, COMPLETED, NEEDS-ACTION
'priority' : '3', #low 9, medium 5, high 3
'id' : '',#it seems this is group id
'value' : 'otherGroup',
'description' : 'default description',
'dueTime' : int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple())),
'triggered' : '0',
'trigger' : 'start',
'triggerOffset' : '-20',
'action' : 'email',#email display
'address' : ''
}

CREATE_TASK_NO_ALARM={
'status' : 'IN-PROCESS',#IN-PROCESS, COMPLETED, NEEDS-ACTION
'priority' : '3', #low 9, medium 5, high 3
'id' : '',#it seems this is group id
'value' : 'otherGroup',
'description' : 'default description'
}

LIST_TASKLIST={}
REPORT_TODOS={
'pageSize' : '50',
'offset' : '0',
'startTime' : int(time.mktime(datetime.datetime.strptime('20130930T093000', '%Y%m%dT%H%M%S').timetuple())),
'endTime' : int(time.mktime(datetime.datetime.strptime('20250930T100000', '%Y%m%dT%H%M%S').timetuple())),
'filter' : '',
'alarmsOnly' : 'false'
}

DEL_TODO={}
UPDATE_TODO={
'status' : 'IN-PROCESS',#IN-PROCESS, COMPLETED, NEEDS-ACTION
'priority' : '3', #low 9, medium 5, high 3
'id' : '',
'value' : 'otherGroup',#it seems this is group id
'description' : 'default description',
'dueTime' : int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple())),
'triggered' : '0',
'trigger' : 'start',
'triggerOffset' : '-20',
'action' : 'display',#email display
'address' : ''
}
UPDATE_TODO_NO_ALARM={
'status' : 'COMPLETED',#IN-PROCESS, COMPLETED, NEEDS-ACTION
'priority' : '5', #low 9, medium 5, high 3
'id' : '',
'value' : 'otherGroup',#it seems this is group id
'description' : 'default description'
}
CREATE_TASKGROUP={}
DEL_TASKLIST={}
UPDATE_TASKLIST={}
TASK_EXPORT={
'componentType' : 'TODO'
}
SHARE_TASKLIST_BY_EMAIL={}
EVENT_READ={}
MAIL_AUTO_REPLY_DISABLE={}

MAIL_AUTO_REPLY_KPN={
'enabled' : 'true',
'message' : 'I am ooo.',
'replyOnce' : 'true',
'original' : 'true',
'altDomains' : '163.com,openwave.com',
'altMessage' : 'I will be back on Monday',
'interval' : '1',
'startDate' : '1416124800000',
'endDate' : '1416211200000'
}

MAIL_GET_QUOTA={}
MOBILE_SIGNATURE_CREATE={}
MOBILE_SIGNATURE_LOAD={}

MAIL_PREFERENCE_LOAD={}
MOBILE_MAIL_PREFERENCE_LOAD={}
MOBILE_SUB_MAIL_PREFERRENCE={#default mobile preference
'emptyTrashOnLogout' : 'false',
'saveOutgoingMessages' : 'false',
'replyQuoting' : 'false',
'mobileAutoCheckInterval' : 'false'
}