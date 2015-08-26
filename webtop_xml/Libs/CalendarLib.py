import datetime, re, os, time, random, copy
import xml.etree.ElementTree as ET
import requests
import RequestLib, CommonLib, WebtopResponseWrap, PrefsLib
from pytz import timezone
from datetime import timedelta, tzinfo

class CalendarLib():
	''' Attributes:
		kargs key from config resource must be exactly same as request attribute name
	    rtkey as attribute from config resource will return request string istead of return response string
	'''
	def __init__(self,url):
		self.url = url
		self.common = CommonLib.CommonLib(self.url)
		self.name = ''
		self.dom = ''
		self.useCalendar = '' 
		self.prefs = ''
		self.tempDict = {}
	
	def _listCalendarID(self, getCalID=False, listFirst = False,getResponseStr = False):
		'''getCalID- receive value is either 'webtop_' or '@' to return the whole calendarID for API attribute value'''
		# name = self.name
		# dom = self.dom
		self.calendarListResp = self.common.request_send(RequestLib.listCalendars)
		calId = re.findall('<calendar id="([^"]*)" url=',self.calendarListResp)
		urlList = re.findall(' url="([^"]*)" ',self.calendarListResp)
		self.tempDict = dict(zip(calId, urlList))
		
		if getCalID:
			for id in calId:
				if getCalID in id.split('/')[-1]:
					self.calid = id
					# self.calIDprefix = id.split(getCalID)[0]
					return self.calid
				elif 'trash' in id:
					pass
		if getResponseStr:
			return self.calendarListResp.replace('><','>\n<')
		if listFirst:
			return calId[0]
		else:
			return calId
	
	def _setTime(self,timeUnit='',plus=0,duration=False):
		self.now = datetime.datetime.now()
		if timeUnit =='month':
			self.endDate = self.now.replace(month=self.now.month+plus).strftime('%Y%m%d')
		elif timeUnit =='day':
			self.endDate = self.now.replace(day=self.now.day+plus).strftime('%Y%m%d')	
		elif timeUnit == 'year':
			self.endDate = self.now.replace(year=self.now.year+plus).strftime('%Y%m%d')
		else:
			self.endDate = self.now.strftime('%Y%m%d')
		if timeUnit == 'hour':
			self.endTime = self.now.replace(hour=self.now.hour+plus).strftime('%H%M%S')
		elif timeUnit == 'minute':
			self.endTime = self.now.replace(minute=self.now.minute+plus).strftime('%H%M%S')
		elif timeUnit == 'second':
			self.endTime = self.now.replace(second=self.now.second+plus).strftime('%H%M%S')
		else:
			self.endTime = self.now.strftime('%H%M%S')
			
		if duration:
			if timeUnit =='month':
				self.startDate = self.now.replace(month=self.now.month-plus).strftime('%Y%m%d')
			elif timeUnit =='day':
				self.startDate = self.now.replace(day=self.now.day-plus).strftime('%Y%m%d')	
			elif timeUnit == 'year':
				self.startDate = self.now.replace(year=self.now.year-plus).strftime('%Y%m%d')
			else:
				self.startDate = self.now.strftime('%Y%m%d')
			if timeUnit == 'hour':
				self.startTime = self.now.replace(hour=self.now.hour-plus).strftime('%H%M%S')
			elif timeUnit == 'minute':
				self.startTime = self.now.replace(minute=self.now.minute-plus).strftime('%H%M%S')
			elif timeUnit == 'second':
				self.startTime = self.now.replace(second=self.now.second-plus).strftime('%H%M%S')
			else:
				self.startTime = self.now.strftime('%H%M%S')
		else:
			self.startDate = self.now.strftime('%Y%m%d')
			self.startTime = self.now.strftime('%H%M%S')
			
		self.localStart = self.startDate + 'T' + self.startTime
		self.localEnd = self.endDate + 'T' + self.endTime
			
	def _setPos(self,day):
		'''return the week day number of the current Month'''
		date = int(day)
		weekN = 0
		if date <= 7:
			return '1'
		else:
			while True:
				if date > 0:
					weekN = weekN + 1
					date = date-7
				else:
					return str(weekN)
		
	def _addReminder(self, request='', t='', type='calendar',returnOffset=False):
		'''<alarm id="" triggered="0" trigger="start" triggerOffset="-2880" action="email" address="vvntest@opal.qa.laszlosystems.com">
			<description>Calendar reminder</description>
			</alarm>'''
		if type == 'calendar':
			eventType = 'event'
		else:
			eventType = 'todo'
		
		timeNumber = int(re.findall('(\d+)',t)[0])
		startDate = self.startDate
		startTime = self.startTime
		endDate = self.endDate
		endTime = self.endTime
		
		if 'm' in t:
			startTime = (self.now+datetime.timedelta(seconds = timeNumber*60+5)).strftime('%H%M%S')
		if 'h' in t:
			timeNumber = timeNumber*60
			startTime = (self.now+datetime.timedelta(minutes = timeNumber+1)).strftime('%H%M%S')
			endTime = (self.now+datetime.timedelta(minutes = timeNumber+2)).strftime('%H%M%S')
		if 'd' in t:
			startDate = (self.now+datetime.timedelta(days = timeNumber)).strftime('%Y%m%d')
			startTime = (self.now+datetime.timedelta(minutes = 1)).strftime('%H%M%S')
			endDate = startDate
			endTime = (self.now+datetime.timedelta(minutes = 2)).strftime('%H%M%S')
			timeNumber = timeNumber*24*60

		kargs={}
		kargs['triggered'] = '0'
		kargs['trigger'] = 'start'
		kargs['triggerOffset'] = '-'+str(timeNumber)
		if returnOffset:
			return kargs['triggerOffset']
		kargs['action'] = 'email'
		kargs['address'] = self.name + self.dom
		kargs['summary'] = 'Calendar reminder'
		request.addElement(xPath= eventType, tag='alarm', attrib=kargs, valueText='')
		request.addElement(xPath= eventType+'/alarm', tag='description', valueText='Calendar reminder')
		
		updateKargs={}
		updateKargs['localStart'] = startDate + 'T' + startTime
		updateKargs['localEnd'] = endDate + 'T' + endTime
		
		request.setElementValue(xPath=eventType, valueText='', attrib=updateKargs)
	
	def _addAttendee(self,request, attendees):
		'''	<attendee id="" name="" email="vvntest2@opal.qa.laszlosystems.com" status="NEEDS_ACTION" type="INTERNAL"/>
			<attendee id="" name="" email="vvntest1@opal.qa.laszlosystems.com" status="NEEDS_ACTION" type="INTERNAL"/>'''
		emailList = attendees.split(' ')
		kargs={}
		for email in emailList:
			kargs['id'] = '' 
			kargs['name'] = '' 
			kargs['email'] = email
			kargs['status'] = 'NEEDS_ACTION'
			kargs['type'] = 'INTERNAL'
			
			request.addElement(xPath='event', tag='attendee', attrib=kargs, valueText='')
			
	def _addOrganizer(self,request):
		'''<organizer id="" name="vvntest@opal.qa.laszlosystems.com" email="vvntest@opal.qa.laszlosystems.com" status="NEEDS_ACTION" type="INTERNAL"/>'''
		kargs={}
		kargs['organizer'] = self.useCalendar.split('/')[4]
		kargs['email'] = self.useCalendar.split('/')[4]
		kargs['status'] = 'NEEDS_ACTION'
		kargs['type'] = 'INTERNAL'
		
		request.addElement(xPath='event', tag='organizer', attrib=kargs, valueText='')
				
	def _getInfofromResp(self,list=[]):
		infoHash = {}
		for k in list:
			response = self.response.replace('><','>\n<')
			infoHash[k] = re.findall( '.*%s="(.*).*'%k, response)[0].split('"')[0]
		return infoHash
	
	def _getTaskGroupID(self, groupName=False):
		'''If given the groupName, then return the group id of this group,
			else, return the first group id from the group list'''
		self.list_task_group()
		if groupName:
			id = re.findall('.*id="(.*)" name="%s".*'%groupName,self.taskGroupResp)[0]
			return id
		else:
			if not re.findall('.*<tasklist calendarId=".*" id="(.*)" name=".*',self.taskGroupResp): #default group is 'otherGroup', not find group value from listTaskLists response
				return 'otherGroup'
			else:
				return re.findall('.*<tasklist calendarId=".*" id="(.*)" name=".*',self.taskGroupResp)[0]
	
	def _setDueTime(self,time):
		timeNumber = int(re.findall('(\d+)',time)[0])
		if 'h' in time:
			timeUnit = 'hour'
		if 'min' in time:
			timeUnit = 'minute'
		if 'd' in time:
			timeUnit = 'day'
		if 'mon' in time:
			timeUnit = 'month'
		if 'y' in time:
			timeUnit = 'year'
		self._setTime(timeUnit,int(timeNumber))
				
	def create_calendar(self,**kargs):
		self.dom = kargs['dom']
		self.name = kargs['name']
		# calIDprefix = self._listCalendarID(getCalID = 'webtop_')
		calName = 'My calendar '+str(random.randint(1,1000))
		color = str(random.randint(1,15))
		CreateCalendarResp = self.common.request_send(RequestLib.calendarCreate%(calName,color))
		CreateCalendarResp = CreateCalendarResp.replace('><','>\n<')
		
		if '<calendar id="' in CreateCalendarResp:
			createdCalID = CreateCalendarResp.split('<calendar id="')[1].split('"')[0] 
			calendarListResp = self._listCalendarID(getResponseStr=True)
		webtopid = createdCalID.split('/')[-1]
		if webtopid in calendarListResp:
			cname = re.findall('.*<calendar id=".*-%s" url=".*-%s" name="(.*)" color=.*'%(webtopid,webtopid), calendarListResp)
			return 'Successfully CREATEd calendar: '+cname[0]
		else:
			raise Exception('Failed to create new caledar, check req: '+RequestLib.calendarCreate%(calName,color))
		
	def delete_calendar(self,**kargs):
		self.dom = kargs['dom']
		self.name = kargs['name']
		calendarListResp = self._listCalendarID(getResponseStr=True)
		calIdList = self._listCalendarID()
		deletedCid = []
		for wholeCid in calIdList:
			if '@' in wholeCid.split('/')[-1] or 'trash' in wholeCid.split('/')[-1]:
				pass
			else:
				cname = re.findall('.*%s.*name="(.*)" color=.*'%wholeCid.replace('?','\?'),calendarListResp)[0]
				calendarDelResp = self.common.request_send(RequestLib.deleteCalendar%(wholeCid,self.tempDict[wholeCid],cname))
				deletedCid.append(wholeCid)
				if not kargs.has_key('all'):
					break
		failedLog = '' # check if all calendar(s) deleted
		calListNewResp = self._listCalendarID(getResponseStr=True)
		for checkDelCid in deletedCid:
			if checkDelCid in calListNewResp:
				failedLog = failedLog + checkDelCid
				if not kargs.has_key('all'):
					break
		if failedLog:
			raise Exception(failedLog + ' failed to be deleted, still exist in calendar list ')
		else:
			return 'All calendar(s) deleted!'+ str(deletedCid)
		
	def update_calendar(self,**kargs):
		''' Optional attribute - newname: new name for calendar update	'''
		self.dom = kargs['dom']
		self.name = kargs['name']
		
		# calendarListResp = self._listCalendarID(getResponseStr=True)
		cid = self._listCalendarID(listFirst=True)
		#return cid
		id = cid
		#id = 'http://%s:5229/calendars/%s%s/'%(self.dom.split('@')[1],self.name,self.dom)+cid
		color = str(random.randint(2,15))
		if kargs.has_key('newname'):
			name = kargs['newname']
		else:
			name = 'random_renamed-'+str(random.randint(1,1000))
		
		calendarDelResp = self.common.request_send(RequestLib.updateCalendar%(id,self.tempDict[id],name,color))
		newListResp = self._listCalendarID(getResponseStr=True)
		if 'name="%s"'%name in newListResp and 'color="%s"'%color in newListResp:
			return 'Successfully UPDATE calendar, name: %s, color: %s'%(name,color)
		else:
			raise Exception('Failed to get new cal name and color from new listCalendar response')
		
	def use_calendar(self,**kargs):
		'''kargs['defaultCalendar'] not empty: return the default calendar id'''
		response = self._listCalendarID(getResponseStr=True).replace('><','>\n<')
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
		if kargs.has_key('defaultCalendar'):
			self.calList = re.findall('<calendar id="(.*@.*/.*@.*)" url=.*',response)
			if kargs.has_key('subscribeDefault'):
				self.calList.pop(0) # for subscribers report the subscribed the default calenar(id with @)
			calid = self._listCalendarID(getCalID = '@')
			# self.useCalendar = calid
			self.defaultCal = calid
		elif kargs.has_key('userCalendar'):
			print 'sdf'
			print response
			self.calList = re.findall('<calendar id="(.*-webtop.*)" url=.*',response)
		self.useCalendar = self.calList[0]
		self.userCal = self.useCalendar
		return self.useCalendar
		
	def list_Calendars(self,**kargs):
		'''kargs['name'],kargs['dom'],   kargs['userCalendar'],kargs['defaultCalendar']: return the user/default calendar id'''
		self.name = self.common.useraddress.split('@')[0]
		self.dom = self.common.useraddress.split('@')[1]
		self.calIdList = []
		if kargs.has_key('defaultCalendar'):
			kargs['defaultCalendar']='true'
			calendar = self.use_calendar(**kargs)
			self.calIdList.append(calendar)
		if kargs.has_key('userCalendar'):
			kargs['userCalendar']='true'
			self.calId = self.use_calendar(**kargs)
			self.calIdList.append(self.calId)
		print 'Calendar number is '+ str(len(self.calIdList))
		return self.calIdList	
	
	def report_events(self,**kargs):
		''' kargs['timeUnit'] = 'month'
		    kargs['time'] = 1'''	
		self._setTime(kargs['timeUnit'],int(kargs['time']),duration=True)
		oringinalReq = RequestLib.reportEvents%(self.startDate,self.endDate)
		
		request = WebtopResponseWrap.WebtopResponseWrap(oringinalReq)
		for calendar in self.calIdList:
			request.addElement(valueText=calendar,xPath='calendar', tag='calendarId')
		reportEventReq = request.toXML()
		self.reportEventResp = self.common.request_send(reportEventReq).replace('><','>\n<')
		eventNumber = re.findall('<events total="(.*)">',self.reportEventResp)
		return str(eventNumber[0])+' events find!'
	
	def import_events_tasks(self,**kargs):
		''' kargs['componentType'] = 'event' or 'todo' 
			kargs['fileid'] '''
		# <request><calendar action="import" calendarId="%s" tasklist="%s" fileid="%s"></calendar></request>
		if kargs['componentType'].lower() == 'event':
			request = RequestLib.importEventTask%(self.useCalendar, kargs['fileid'])
		elif kargs['componentType'].lower() == 'todo':
			self.use_calendar(defaultCalendar='true')
			if kargs.has_key('defaultGroup'):
				group = 'otherGroup'
			else:
				self.list_task_group()
				group = re.findall('.*<tasklist.*name="(.*)" />.*',self.taskGroupResp)[0]
			request = RequestLib.importEventTask%(self.useCalendar, kargs['fileid'])
			request = request.replace('></calendar>',' tasklist="%s" ></calendar>'%group)
		else:
			raise Exception("wrong kargs['componentType']")		
		
		response = self.common.request_send(request)
		if '<calendar action="import" />' not in response:
			raise Exception('Failed to import '+kargs['componentType'])
		else:
			return kargs['componentType']+ ' importeded!'
	
	def export_events_tasks(self, **kargs):
		'''	kargs['componentType']= event,todo
			url=${contact_export} '''
		url = kargs['url'].replace('download/','download?') + kargs['componentType'] + '.ics'
		data = {}
		d= '<resource resolver="calendar" calendarId="%s" filename="%s.ics" componentType="%s"/>' 
		if kargs['componentType'].lower() == 'event':
			data['r'] = d%(self.useCalendar, kargs['componentType'], kargs['componentType'].upper())
		elif kargs['componentType'].lower() == 'todo':
			self.use_calendar(defaultCalendar='true')
			if kargs.has_key('defaultGroup'):
				group = 'otherGroup'
			else:
				self.list_task_group()
				group = re.findall('.*id="(.*)" name=*',self.taskGroupResp)[0]
			d=d.replace('/>',' tasklist="%s"/>'%group)
			data['r'] = d%(self.useCalendar, kargs['componentType'], kargs['componentType'].upper())
		else:
			raise Exception("wrong kargs['componentType']")
			
		r = self.common.session.post(url,data)
		if 'error' in r.text:
			raise Exception('Error:'+r.text)
		else:
			return kargs['componentType']+ ' exported!'
	
	def delete_events(self, **kargs):
		''' kargs['timeUnit'] = 'month'
		    kargs['time'] = 1'''
		self.report_events(**kargs)
		allEvents = WebtopResponseWrap.WebtopResponseWrap(self.reportEventResp)
		eventList = allEvents.getElementList('calendar/events/event')
		passLog = 'Delete events passLog'
		failedLog = ''
		donetitle = ''
		for event in eventList:
			calendarId = event.getTextValue('./@calendarId')
			id = event.getTextValue('./@id')
			summary = event.getTextValue('./@summary')
			if self.useCalendar not in event.toXML():
				pass
			
			elif summary in donetitle:
				pass

			else:
				kargs['affects']="all"
				delEventReq = self.common.request_send(RequestLib.deleteEvent%(calendarId,id,kargs['affects'],event.toXML()))
				if 'calendar action="deleteEvent"' in delEventReq:
					passLog = passLog + '%s is deleted \n'%summary
				else:
					failedLog = failedLog + '%s delete failed \n'%summary
				donetitle = donetitle +'///'+ re.findall('.* summary="(.*)" url=.*',event.toXML().replace('><','>\n<'))[0]
				pass
				
		if failedLog:
			raise Exception ('Failed to delete all events')
		else:
			return 'Successfully deleted events!'
		
	def create_event_categories(self,**kargs):
		'''attendees=${common_to}${common_domain}
			'''
		if kargs.has_key('allcategories'):
			categories = ['general','invite', 'work', 'school', 'red','yellow', 'green', 'birthday', 'anniversary', 'date', 'vacation', 'fun', 'bills', 'phone', 'doctor', 'flag', 'pet', 'sport']
		else:
			categories = ['general']	
		location = 'bj'
		description = 'some description'
		passLog = 'Pass log:\n'
		faileLog = ''
		for c in categories:
			self._setTime('hour',1)
			title = 'New event %s on %s'%(c,str(self.now))
			oringinalReq = RequestLib.createEvent%(title,location,self.localStart,'False',self.useCalendar,self.localEnd,description,c)
			request = WebtopResponseWrap.WebtopResponseWrap(oringinalReq)
			if kargs.has_key('attendees'):
				self._addOrganizer(request)
				self._addAttendee(request,attendees=kargs['attendees'])
				del kargs['attendees']
			if kargs.has_key('reminder'):
				self._addReminder(request,t=kargs['reminder'])	
				del kargs['reminder']
			self.request = request.toXML()
			
			if kargs.has_key('forUpdate'):
				del kargs['forUpdate']
				self.request = self.request.replace('createEvent','updateEvent')
				self.request = self.request.replace('summary="','summary="[Updated]')
				return 'Event is updated'
			else:
				self.response = self.common.request_send(self.request)
			
			for i in (title,location,self.useCalendar,description,c):
				if i in self.response:
					if kargs.has_key('returnTitle'): # return the event title out for receiver invitation check
						self.eid = re.findall(' id="(.*)" calendarId.*',self.response)[0]
						# print 'eventId is '+str(self.eid)
						return title
				else:
					faileLog = faileLog + '%s not in response;'%i + title + '\n'
			passLog = passLog + title +','+ c +'\n'	
			
		if faileLog:
			raise Exception('Failed to create event' + faileLog)
		else:
			return 'Categorie(s) are created\n' + passLog
			
	def create_recurrent_Events(self,**kargs):
		'''	Attributes:
			eg1, by duration 5 days: freq="weekly" count="5" interval="1" dayList="SU,MO,TU,WE,TH,FR,SA"
			eg2, by till date: freq="daily" count="-1" interval="2" untilMonth=3
			eg3. attendees=${common_to}${common_domain}  reminder=3m
			'''
		location = 'bj'
		description = 'some description'
		self._setTime('hour',1) #set current day end time
		title = 'Recur: %s'%str(self.now)
		updatedTitle = '_Updated_'
		oringinalReq = RequestLib.createEvent%(title,location,self.localStart,'False',self.useCalendar,self.localEnd,description,'')

		# set attendee(s) or reminder
		request = WebtopResponseWrap.WebtopResponseWrap(oringinalReq)
		if kargs.has_key('attendees'):
			self._addOrganizer(request)
			self._addAttendee(request,attendees=kargs['attendees'])
			del kargs['attendees']
		if kargs.has_key('reminder'):
			self._addReminder(request,t=kargs['reminder'])
			del kargs['reminder']
						
		# set local until date - 'Ends on specific date'
		if kargs.has_key('untilMonths'):
			kargs['localUntil'] = str(int(self.localStart.split('T')[0])+100*int(kargs['untilMonths']))+'T235959'
			del kargs['untilMonths']
			updatedTitle = 'untilMonths ' + updatedTitle
		if kargs.has_key('untilYears'):	
			kargs['localUntil'] = str(int(self.localStart.split('T')[0])+10000*int(kargs['untilYears']))+'T235959'		
			del kargs['untilYears']
			updatedTitle = 'untilYears ' + updatedTitle
			kargs['count']= '-1'
			kargs['setPos']=''
			kargs['dayList']=''

		addAttr = {}
		if kargs['freq']=='yearly': # set for YEARLY recurrent - have to be at this day of year
			addAttr['monthDayList'] = self.now.strftime('%d')
			updatedTitle = 'ThisDayofYear ' + updatedTitle
		if kargs.has_key('DayofMonth'):	# set for MONTHLY recurrent - 'This day of month'
			addAttr['monthDayList'] = self.now.strftime('%d')
			del kargs['DayofMonth']
			updatedTitle = 'ThisDayofMonth ' + updatedTitle
		if kargs.has_key('DayofWeek'):	# set for MONTHLY recurrent - 'This day of week'
			weekday = self.now.strftime('%w')
			addAttr['dayList'] = ['MO','TU','WE','TH','FR','SA','SU'][int(weekday)-1]
			addAttr['setPos'] = self._setPos(self.now.strftime('%d'))
			del kargs['DayofWeek']
			updatedTitle = 'ThisDayofWeek ' + updatedTitle
		
		request.addElement(xPath='event', tag='recurrence', attrib=kargs, valueText='')
		
		if kargs.has_key('dayList'):	# set dayList for WEEKLY-'On days', or for MONTHLY-'This day of week'
			request.setElementValue(xPath='event', valueText='recurrence', attrib={'dayList':kargs['dayList']})	

		request.setElementValue(xPath='event/recurrence', valueText='', attrib=addAttr)
		self.request = request.toXML()
		
		if kargs.has_key('forUpdate'):
			del kargs['forUpdate']
			self.request = self.request.replace('Recur:',updatedTitle)
			self.request = self.request.replace('createEvent','updateEvent')
			self.request = self.request.replace('summary="','summary="[Updated]')
			print 'being update...'
		else:
			self.response = self.common.request_send(self.request)
			expect = '<recurrence freq="%s" interval="%s"/>'%(kargs['freq'],kargs['interval'])
			failelog = ''
			if kargs.has_key('returnTitle'): # return the event title out for receiver invitation check
				self.eid = re.findall(' id="(.*)" calendarId.*',self.response)[0]
				return title
			for i in range(len(kargs)):
				if 'freq="yearly"' in self.response and 'localUntil=' in self.response:
					break # yearly repeat until N years - original manual response doesnot have count="-1" and setPos="", so skip to check this
				elif '%s="%s"'%(kargs.keys()[i],kargs.values()[i]) in self.response:
					pass
				else:
					failelog = failelog + '%s="%s"'%(kargs.keys()[i],kargs.values()[i])
			if failelog:
				raise Exception('Failed to created event with '+failelog+' for '+str(kargs))
			return 'Recurrent event created'+str(kargs)
		return 'No event created/Updated'
	
	def get_new_eventId(self):
		eid = re.findall('id="(.*)" calendarId', self.response)[0] #response should be from create event request
		return eid
		
	def read_event(self,**kargs):
		eventId = self.get_new_eventId()
		self.readEventResp = self.common.request_send(RequestLib.readEvent%(self.useCalendar, eventId))
		if '<calendar action="readEvent">' in self.readEventResp:
			return 'event %s could be read'%eventId
		else:
			raise Exception('Failed to read the %s event'%eventId)
	
	def update_event(self,**kargs):
		'''kargs['affects']=instance/all'''
		calendarAttr = {} # set actual key/value into kargs which need update
		calendarAttr['notifyType'] = 'CANCEL_EVENT'
		if kargs.has_key('affects'):
			calendarAttr['affects'] = kargs['affects']
			del kargs['affects']
		else:
			calendarAttr['affects'] = 'all'
		calendarAttr['calendarId'] = self.useCalendar
		eventAttr = self._getInfofromResp(['id'])
		eventAttr.update(self._getInfofromResp(['startTime']))
		eventAttr.update(self._getInfofromResp(['endTime']))
	
		kargs['forUpdate'] = 'true'
		self.create_recurrent_Events(**kargs) # get request xml as template
		del kargs['forUpdate']
		
		updateReq = WebtopResponseWrap.WebtopResponseWrap(self.request) # piece kargs and xml as request and send
		updateReq.setElementValue(xPath='.', valueText='', attrib=calendarAttr)
		updateReq.setElementValue(xPath='event', valueText='', attrib=eventAttr)
		resposne = self.common.request_send(updateReq.toXML()) 
		failLog = ''
		for k in kargs:
			if kargs[k] not in resposne:
				failLog = failLog + kargs[k] + ', '
		if failLog:
			raise Exception('failed to update: '+failLog )
		else:
			return 'Successfully update calendar event for%s'%kargs
		
	def send_invitation(self):
		sendReq = WebtopResponseWrap.WebtopResponseWrap(self.request.replace('createEvent','sendInvite'))
		calendarNodeH = self._getInfofromResp(['calendarId'])
		calendarNodeH['notifyType']='CREATE_EVENT'
		sendReq.setElementValue(xPath='.', valueText='', attrib=calendarNodeH)
		
		getEventH = self._getInfofromResp(['startTime','endTime','id'])
		sendReq.setElementValue(xPath='event', valueText='', attrib=getEventH)
		response = self.common.request_send(sendReq.toXML())
		if '<status>ok</status>' in response:
			return 'Successfully send invitation'
		else:
			raise Exception('Failed to send invitation')
		
	def response_invitation(self, **kargs):
		'''Two kargs:  receiver=${common_to}  response=Maybe'''
		optH = {'yes':'1', 'no':'2', 'maybe':'3'}
		opt = optH[kargs['response'].lower()]
		calid = self.useCalendar
		ownerid = ownername = (self.name+self.dom).lower()
		email = kargs['receiver']+self.dom
		request = RequestLib.updateRsvpReq%(opt,calid,ownerid,ownername,self.eid,email)
		response = self.common.request_send(request)
		if '<calendar action="updateRsvp" />' in response:
			return 'Invitation response sent with: '+ kargs['response'].lower()
		else:
			raise Exception('Failed to send invitation response: '+ kargs['response'].lower())
		
	def check_invitation_event(self, **kargs):
		''' kargs['addToCalendar']
			kargs['subject']
			kargs['timeUnit'] = 'month'
		    kargs['time'] = 1'''
		kargs['defaultCalendar']='true'
		calendars = self.list_Calendars(**kargs)
		eventN = self.report_events(**kargs)
		if kargs.has_key('addToCalendar'):
			if kargs['subject'] in self.reportEventResp:
				return 'Invitation (%s) is added to default calendar'%kargs['subject']
			else:
				raise Exception('Invitatoin (%s) is not added to default calendar'%kargs['subject'])
		else:
			if not kargs['subject'] in self.reportEventResp:
				return 'Invitation (%s) is not added to default calendar'%kargs['subject']
			else:
				raise Exception('Invitatoin (%s) is added to default calendar'%kargs['subject'])
		
	def create_task_group(self, **kargs):
		'''Attrs: 'returnName' (optional) - return task group name'''
		groupName = 'group'+str(random.randint(1,1000))
		self.dom = kargs['dom']
		self.name = kargs['name']
		calid = self._listCalendarID(getCalID = '@')
		self.calendarId = calid
		#self.calendarId = 'http://%s:5229/calendars/%s%s/'%(self.dom.split('@')[1],self.name,self.dom) + calid
		
		createTaskGroupReq = RequestLib.createTaskGroup%(self.calendarId,self.calendarId,groupName)
		response = self.common.request_send(createTaskGroupReq)
		if kargs.has_key('returnName'):
			return re.findall('.*name="(.*)".*',response)[0]
		else:
			return response
		
	def list_task_group(self, **kargs):
		'''Attr - 'check' to check the content from listTaskLists response ,ex. check=${groupName}'''
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
		calid = self._listCalendarID(getCalID = '@')
		self.calendarId = calid
		#self.calendarId = 'http://%s:5229/calendars/%s%s/'%(self.dom.split('@')[1],self.name,self.dom) + calid
		self.taskGroupResp = self.common.request_send(RequestLib.listTaskLists%self.calendarId)

		if kargs.has_key('check'):
			if 'name="%s"'%kargs['check'] in self.taskGroupResp:
				return 'Checked task group [%s] is created in task group list'+kargs['check']
			else:
				raise Exception('Failed to check task group %s after created'%kargs['check'])
				
		if kargs.has_key('checkDeleted'):
			if 'name="%s"'%kargs['checkDeleted'] not in self.taskGroupResp:
				return 'Task group [%s] is actually deleted from group list'%kargs['checkDeleted']
			else:
				raise Exception('Task group [%s] still exist'%kargs['checkDeleted'])		
			
		else:
			self.allGroupResp = WebtopResponseWrap.WebtopResponseWrap(self.taskGroupResp)
			self.groupList = self.allGroupResp.getElementList('calendar/tasklist')
			return len(self.groupList)
		
	def update_task_group(self,**kargs):
		'''kargs['groupName'],kargs['newName']'''
		groupName = kargs['groupName']
		newName = kargs['newName']
		id = self._getTaskGroupID(groupName)
		response = self.common.request_send(RequestLib.updateTaskList%(self.calendarId,self.calendarId,id,newName ))
		if newName not in response:
			raise Exception('Failed to update %s to %s'%(groupName,newName))
		else:
			return newName
	
	def delete_task_groups(self,**kargs):
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
		deletedGroups = 'Successfully deleted: '
		failedlog = ''
		for group in self.groupList:
			response = self.common.request_send(RequestLib.deleteTaskList%(self.calendarId,group.toXML()))
			groupName = group.getTextValue('./@name')
			deletedGroups = deletedGroups + groupName + ', '
			if '<calendar action="deleteTaskList" />' not in response:
				failedlog = failedlog + group + ', '
			if not kargs.has_key('all'):
				break
		if failedlog:
			raise Exception('Failed to delete '+ failedlog)
		return deletedGroups
		
	def create_task(self,**kargs):
		'''priority: 9 Low, 5 Normal, 3 High
			kargs['forUpdate'] is only for updating non-reminder tasks
			kargs: duetime=3h, reminder=1h, status=IN-PROCESS, priority=3 groupName(opthinal)'''
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
			del kargs['dom']	
			del kargs['name']	
		kargs['summary'] = 'task' + str(random.randint(1,1000))
		kargs['defaultCalendar'] = True
		kargs['calendarId'] = self.use_calendar(**kargs)
		del kargs['defaultCalendar']	
		if kargs.has_key('groupName'):
			groupName = kargs['groupName']
			del kargs['groupName']
		else:
			groupName = ''
		
		kargs['value'] = self._getTaskGroupID(groupName)
		if kargs.has_key('localDue'):
			self._setDueTime(time=kargs['localDue']) 
			kargs['localDue'] = self.localEnd 
		if kargs.has_key('reminder'):
			t=kargs['reminder']
			del kargs['reminder']
			self.request = self.common.request_send(RequestLib.createTask, kargs,getRes=True)
			addReminderReq = WebtopResponseWrap.WebtopResponseWrap(self.request)
			self._addReminder(addReminderReq,t,type='task')
			self.request = addReminderReq.toXML()
			self.response = self.common.request_send(self.request)
		else:
			if kargs.has_key('forUpdate'): # get original request for update
				del kargs['forUpdate']
				self.request = self.common.request_send(RequestLib.createTask, kargs,getRes=True)
			self.response = self.common.request_send(RequestLib.createTask, kargs)
		
		failLog = ''
		for key in kargs:
			if kargs[key] in self.response:
				pass
			else:
				failLog = failLog + kargs[key] +'\n'
				# return kargs[key]
		if not failLog:
			print 'Task created with '+str(kargs)
			return kargs['summary']
		else:
			raise Exception ('Failed to created in'+failLog)
				
	def get_tasks(self,**kargs):
		'''return list of WebtopResponseWrap object'''
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
		kargs['defaultCalendar'] = 'true'
		self.calendarId = self.use_calendar(**kargs)
		TaskResp = self.common.request_send(RequestLib.reportToDos%self.calendarId)
		if kargs.has_key('checkTask'):
			if kargs['checkTask'] in TaskResp:
				return 'Task [%s] is found from task list'%kargs['checkTask'] 
			else:
				raise Exception('Task [%s] is not found from task list'%kargs['checkTask'] )
			
		allTodoResp = WebtopResponseWrap.WebtopResponseWrap(TaskResp)
		self.todoList = allTodoResp.getElementList('calendar/todos/todo')
		return len(self.todoList)
		
	def delete_tasks(self,**kargs):
		if kargs.has_key('dom') and kargs.has_key('name'):
			self.dom = kargs['dom']
			self.name = kargs['name']
		self.get_tasks()
			
		deletedTodos = 'Successfully deleted: '
		for todo in self.todoList:
			response = self.common.request_send(RequestLib.deleteToDo%(self.calendarId,todo.toXML()))
			summary = todo.getTextValue('./@summary')
			deletedTodos = deletedTodos + summary + ', '
		return deletedTodos
		
	def update_task(self,**kargs):
		todoid = re.findall('.*<todo summary=".*" id="(.*)" calendarId.*',self.response.replace('><','>\n<'))[0]
		kargs['id'] = todoid
		request = self.request.replace('createToDo','updateToDo')
		updateReq = WebtopResponseWrap.WebtopResponseWrap(request)
			
		alarmAttri = {}
		if kargs.has_key('reminder'):
			alarmAttri['triggerOffset'] = self._addReminder(request,t=kargs['reminder'],returnOffset=True)
			updateReq.setElementValue(xPath='todo/alarm', valueText='', attrib=alarmAttri)
			del kargs['reminder']
		if kargs.has_key('localDue'):
			self._setDueTime(time=kargs['localDue']) 
			kargs['localDue'] = self.localEnd 
		
		updateReq.setElementValue(xPath='todo', valueText='', attrib=kargs)
		resposne = self.common.request_send(updateReq.toXML())
		failLog = ''
		for k in kargs:
			if kargs[k] not in resposne:
				failLog = failLog + kargs[k] + ', '
		if failLog:
			raise Exception('failed to update: '+failLog )
		else:
			return 'Successfully update task for%s'%kargs
		
	def advanced_search(self,**kargs):
		'''	action, starYMD, endYMD, (optional)categories, (optional)alarmsOnly   
			(optional)filter,calendarID(one or more)	'''
		if kargs['action'] == 'allActions': # action
			actions = ['reportEvents','reportToDos']
		else:
			actions = [kargs['action']]
		kargs['localStart'] = kargs['starYMD'] # localStart
		kargs['localEnd'] = kargs['endYMD'] # localEnd
		if kargs.has_key('categories'):  # (optional)categories
			kargs['categories'] = kargs['categories'].upper()
		calendarIds = []  # calendarID(one or more)
		if kargs['calendar'] == 'default':
			calendarIds = [self.defaultCal]
		if kargs['calendar'] == 'user':
			calendarIds = [self.userCal]
		if kargs['calendar'] == 'all':
			calendarIds = [self.defaultCal, self.userCal]
		
		del kargs['starYMD'],kargs['endYMD'],kargs['action']
		originalReq = self.common.request_send(RequestLib.advancedSearch, kargs, getRes=True)
		for action in actions:	#  add calendarIds for each action and send request
			wrapReq = WebtopResponseWrap.WebtopResponseWrap(originalReq)
			actionKargs = {'action':action}
			wrapReq.setElementValue(xPath='calendar', valueText='', attrib=actionKargs)
			if len(calendarIds) >1: # search in multi-calendars -> add nodes
				for calendar in calendarIds:
					wrapReq.addElement(xPath='calendar', tag='calendarId', attrib={}, valueText=calendar)#,
			else: # search in one calendar -> set attribute
				wrapReq.setElementValue(xPath='calendar', valueText='', attrib={'calendarId':calendarIds[0]})
			
			response = self.common.request_send(wrapReq.toXML())
			if 'total="' in response:
				return re.findall('<.* (total="\d+")>',response)
			else:
				raise Exception ('Failed to get response from advance search')
		
	def set_calendar_prefs(self,**kargs):
		'''eg. kargs['all'] = defaultview, kargs['all'] = endTimeOfDay
			eg.	kargs['defaultview'] = 'list'	kargs['TaskReminderUnit'] = '60' '''
		all_defaultview = ['day','week','month','list']
		all_StartTimeOfDay = range(23)
		all_endTimeOfDay = range(1,24)
		all_weekstart = [0,1] # sunday-0, monday-1
		all_timeinterval = [0,1,59,60,61,119,120,121,23*60,24*60] # event duration
		all_remindertime = all_TaskReminderUnit = [0,1,59,60,61,119,120,121,23*60,24*60,25*60+1,2*24*60,30*24*60] # event/task reminder
		all_TaskViewType = ['single', 'taskgroup']
		all_TaskSortType = ['priority', 'duedate', 'needaction', 'incomplete', 'complete', 'title' ]
		request = WebtopResponseWrap.WebtopResponseWrap(RequestLib.prefsSet_template)
		if kargs.has_key('all'):
			valueL = eval('all_'+kargs['all'])
			if kargs['all'] in ['defaultview','weekstart','timeinterval']:
				nameH = {'name' : 'calendar.' + kargs['all']}
			else:
				nameH = {'name' : 'attr.user.' + kargs['all']}
			if kargs['all'] == 'StartTimeOfDay':
				request.addElement(xPath='prefs', tag='prefs', attrib = {'name':'attr.user.endTimeOfDay'}, valueText = '23')
				self.common.request_send(request.toXML())
				request.removeElement(xPath='prefs/prefs',index=0)
			if kargs['all'] == 'endTimeOfDay':
				request.addElement(xPath='prefs', tag='prefs', attrib = {'name':'attr.user.StartTimeOfDay'}, valueText = '0')
				self.common.request_send(request.toXML())
				request.removeElement(xPath='prefs/prefs',index=0)
			for value in valueL:
				request.addElement(xPath='prefs', tag='prefs', attrib = nameH, valueText = str(value))
				self.common.request_send(request.toXML())
				time.sleep(1)
				request.removeElement(xPath='prefs/prefs',index=0)
			return (nameH['name'], valueL)
			
		else:
			for attrK in kargs:
				if attrK in ['defaultview','weekstart','timeinterval']:
					nameH = {'name' : 'calendar.' + attrK}
				else:
					nameH = {'name' : 'attr.user.' + attrK}
				request.addElement(xPath='prefs', tag='prefs', attrib = nameH, valueText = kargs[attrK])
				self.common.request_send(request.toXML())
				request.removeElement(xPath='prefs/prefs',index=0)
			return kargs
			
	def list_subscribed_calendars(self):
		self.subscribedCals = self.common.request_send(RequestLib.listCalendars)
		self.subscribedCalNodes = re.findall('<calendar id=.*personal="false".*/>', self.subscribedCals.replace('><','>\n<'))
		# self.subscribedIds = re.findall('calendar id="(.*)" url=".*" name=".* personal="false" .*', self.subscribedCals.replace('><','>\n<'))
		# self.subscribedNames = re.findall('calendar id=".*" url=".*" name="(.*)" color=".* personal="false" .*', self.subscribedCals.replace('><','>\n<'))
		return 'Subscribed calendar list Nodes:' + str(self.subscribedCalNodes)
		
	def delete_subscribed_calendars(self,**kargs):
		deleteCal = '<calendar action="deleteCalendar" timezone="" limit="25">%s</calendar>'
		failedLog = ''
		for calNode in self.subscribedCalNodes:
			response = self.common.request_send(deleteCal%calNode)
			if '<calendar action="deleteCalendar" />' not in response:
				failedLog = failedLog + calNode +',\n '
			if not kargs.has_key('all'):
				break
		if failedLog:
			raise Exception('failed to delete calendars: '+failedLog)
		return 'Deleted calendar(s)'
	
	def share_calendar(self,**kargs):
		''' kargs['level'] - read, readwrite
			kargs['receiveraddr'] - receiver
			kargs['allowAnyone'] - optional
			##### NOTREADY -> veiw and edit (view only works and api is same)
			type: anyone, anyInternal, external, internal, undefined
			level: freebusy, read, readwrite, admin, errorLevel'''
		self.calOwner = self.name+self.dom
		request = RequestLib.shareCalenar%(self.useCalendar,self.calOwner, kargs['level'], kargs['receiveraddr'])
		self.sharedName = re.findall('.*calendar id="%s" url=".*" name="(.*)" color=".*" shown=.*'%self.useCalendar, self.calendarListResp.replace('><','>\n<'))[0]
		print request
		if kargs.has_key('allowAnyone'): # <user type="anyone" level="read"/>
			request = WebtopResponseWrap.WebtopResponseWrap(request)
			addAttr = {'type':'anyone','level':'read'}
			request.addElement(xPath='accessList/users', tag='user', valueText="", attrib = addAttr)
			request = request.toXML()
		response = self.common.request_send(request)
		if '<status>ok</status>' in response:
			return 'Calendar %s shared to %s is OK'%(self.sharedName, kargs['receiveraddr'])
		else:
			raise Exception('Failed to share calendar')
	
	def save_shared_calendar(self,**kargs):
		''' calid="%s" kargs['ownername'] '''
		request = RequestLib.saveSharedCalendar%(self.useCalendar, self.calOwner, self.sharedName)
		response = self.common.request_send(request)
		if 'calendar action="saveSharedCalendar"' in response:
			return 'Shared calendaer %s saved to %s'%(self.sharedName, self.calOwner)
		else:
			raise Exception('Failed to save shared calendar %s to %s'%(self.sharedName, self.calOwner))
	
	def check_saved_calendar(self, **kargs):
		if kargs.has_key('defaultCalendar'):
			kargs['subscribeDefault']=True # if subscribed a defult calendar, report event with the second default format '@ 'id, control use_calendar
		self.list_Calendars(**kargs)
		# self.calendarListResp = self.common.request_send(RequestLib.listCalendars).replace('><','>\n<')
		if self.sharedName in self.calendarListResp:
			return 'Shared calendar %s is found from calendar list'%self.sharedName
		else:
			raise Exception('Shared calendar %s is actually not found from calendar list'%self.sharedName)
	
	def subscribe_calendar(self, **kargs):
		# return self.useCalendar
		self.sharedName = self.useCalendar
		request = RequestLib.subscribeCalendar%(self.useCalendar, kargs['name'])
		response = self.common.request_send(request)
		if self.useCalendar in response:
			return '%s is subscribed'%self.useCalendar
		else:
			raise Exception('%s is NOT subscribed'%self.useCalendar)
	
	
	def try_edit_event(self, **kargs):
		'''need one kargs: readOnly, true or no kargs'''
		# # # color = str(random.randint(2,15))
		# # request = RequestLib.updateCalendar.replace('published="true"','published="false"').replace('personal="true"','personal="false"')
		# if kargs.has_key('readOnly'):
			# request = request.replace('readOnly="false"','readOnly="true"')
		# response = self.common.request_send(request%(self.useCalendar, self.useCalendar, self.sharedName+'-edited',color))
		
		eventNode = re.findall('(<event .*[\n.]*)', self.reportEventResp)[0]
		eventId = re.findall('summary="test" id="(.*)" calendarId', self.reportEventResp)
		eventForUpdate = '<calendar action="updateEvent" calendarId="%s" id="%s" timezone="" affects="instance">%s</event></calendar>'%(self.useCalendar, eventId, eventNode)
		updateReq = eventForUpdate.replace('summary="','summary="Updated_')
		response = self.common.request_send(updateReq)
		
		if not kargs.has_key('readOnly'):
			if '<calendar action="updateEvent">' in response:
				return 'Received saved calendar updated!'
			else:
				raise Exception('Received saved calendar failed to be updated!')
		else:
			pass # to catch webtop error in future
	
#-----time zone--------
	def get_hk_timestamp_cal(self,**kargs):
		self.prefs = PrefsLib.PrefsLib(self.url)
		exec "self.timestamp = self.prefs.get_field_value(response=self.%s, fieldName=kargs['stampName'])"%kargs['response'] #'sent-date'
		self.timestamp = self.timestamp+'000'
		return 'HK timestamp for [%s] is: %s'%(kargs['stampName'], self.timestamp)

	def expt_all_timezones_cal(self,**kargs):
		# prefs = PrefsLib.PrefsLib(self.url)
		timezones = self.prefs.list_timezones()
		self.send_tzExp = self.prefs.return_locals_expect(hkTimeStamp= float(self.timestamp), checkFormat=kargs['format'], timezones=timezones)
		return 'Expectations are ready'
		
	def check_time_zones_cal(self,**kargs):
		''' kargs['fieldName'] - actual field name from response'''
		# prefs = PrefsLib.PrefsLib(self.url)
		failLog = ''
		print 'checking timezones...'
		for zone in self.send_tzExp:
			self.prefs.set_timezones(specific=zone['name'])
			exec "self.%s(**kargs)"%kargs['function']
			exec "gotTimeField = self.prefs.get_field_value(response=self.%s, fieldName=kargs['fieldName'])"%kargs['response']
			
			if not str(zone['expTime']) in gotTimeField:
				if abs(int(zone['expTime'].split('T')[1]) - int(gotTimeField.split('T')[1])) < 2500: # gap should be within 25min
					pass
				else:
					failLog = failLog + '[%s] %s expect %s, but got %s \n'%(zone['name'], kargs['fieldName'], str(zone['expTime']), gotTimeField)
		if failLog:
			raise Exception(failLog)
		return 'All time zones checked successfully.\n'
		
	def check_hk_time_cal(self, **kargs):
		if not self.prefs:
			self.prefs = PrefsLib.PrefsLib(self.url)
		exec "gotTime = self.prefs.get_field_value(response=self.%s, fieldName=kargs['fieldName'])"%kargs['response']

		gotDateTime = datetime.datetime.strptime(gotTime, kargs['format'])
		timedelta = (datetime.datetime.now()-gotDateTime).seconds
		print 'time delta is '+str(timedelta)
		if not timedelta < 5*60: # gap is in 5mins
			print 'time delta is %s mins'%str(timedelta/60)
			raise Exception('Gap on %s between PC local time and response is longer than 30mins'%kargs['fieldName'])
		return 'HK time is correnctly checked on '+kargs['fieldName']
		
	
# -----------Max Quota Test-------------
	def create_max_calendar(self,**kargs):
		if not kargs.has_key('calendarMax'):
			raise Exception('Missing calendarMax in parameters!')
		exceedNumber = int(kargs['calendarMax']) + 1
		for i in range(exceedNumber):
			try:
				self.create_calendar(name=kargs['name'],dom=kargs['dom'])
				print 'create number '+str(i)
			except Exception,ex:
				if (i == int(kargs['calendarMax'])): #to do:need to assert the error msg
					return 'One more than Max raise exception, case pass!'
				else:
					print 'number '+str(i)+' failed'
					raise ex
		raise Exception('Exceed the nested layer limitation %s! No error found in response.'%str(exceedNumber))
			
			
			


# newfile = open('E:\\Repositaries\\robot\\workspace\\Libs\\tmp.txt','w')
# newfile.write(res.read()) # str(re.findall('.*(<todo summary.*/todo>).*',TaskResp))
# newfile.close()