import datetime, re, os, sys, time, random, copy, requests
import xml.etree.ElementTree as ET
import WebtopResponseWrap
from pytz import timezone
from datetime import timedelta, tzinfo
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Calendar import Calendar
from GlobalHelper import GlobalHelper
import json, SysUtils



class CalendarLib(Calendar):
	def __init__(self,url):
		Calendar.__init__(self, url)
		self.url = url
		self.GHelper = GlobalHelper()
		self.reqBuilder = SysUtils.getRequestBuilder()
		
	def get_calendar_param_by_key(self, **kargs):
		'''
		kargs['res'] -> {
			"id" : "http://msscalpab:5229/calendars/webtop8@openwave.com/webtop_14bc54f58a9",
			"name" : "create test2",
			"color" : null,
			"visible" : true,
			"primary" : false,
			"personal" : true,
			"readOnly" : false,
			"sharingUrl" : "http://proxyHost:1234/calendars/webtop8@openwave.com/webtop_14bc54f58a9"
		  }
		kargs['key'] -> eg. "name" means check by name
		kargs['exp_value'] -> expect a value of key, eg. "new cal" means calendar name
		kargs['get'] -> the param expect to get, eg. "id" means to get calendar id
		'''
		calendar = eval(kargs['res'])
		if calendar[kargs['key']] == kargs['exp_value']:
			return calendar[kargs['get']]
		else:
			raise Exception('Failed to get %s by %s'%(kargs['get'],kargs['key'] ))
	
	def get_calendar_id_by_name(self, **kargs):
		res = self.list_calendar()
		result_id = utils.getIdListByName(name=kargs['name'], res=str(res))
		if kargs.has_key('one_string'):
			return result_id[0]
		if kargs.has_key('index'):
			index = int(kargs['index'])
			return result_id[index]
		return result_id
		
	
	def del_all_calendars(self):
		res = self.list_calendar()
		cal_list = eval(res)
		print type(cal_list)
		for cal in cal_list:
			if 'main calendar' not in cal['name']:
				kargs = {'params.id': cal['id']}
				self.del_calendar(**kargs)
	
	def get_oringinal_event_ids(self, **kargs):
		'''	kargs['res'] -> report event response
			return ids list, if there's a recurrent event, just return the oringinal one '''
		eventRes = eval(kargs['res'])['events']['results']
		ids = []
		for event in eventRes:
			if event.has_key('recurrence') and event.has_key('recurrenceOf'):
				pass
			elif event['@type'] == 'Event':
				ids.append(event['uid'])
		if kargs.has_key('index'):
			index = int(kargs['index'])
			return ids[index]
		return ids
		
	def get_recurrence_master_event_ids(self, **kargs):
		'''	kargs['res'] -> report event response
			return ids list, only for a recurrent event, just return the oringinal ones '''
		eventRes = eval(kargs['res'])['events']['results']
		ids = []
		for event in eventRes:
			if not event.has_key('recurrenceOf') and event.has_key('recurrence') and event['@type'] == 'Event':
				ids.append(event['uid'])
		return ids
	
	def get_recurrence_sub_event_ids(self, **kargs):
		'''	kargs['res'] -> report event response
			kargs['masterId'] -> only one master event Id
			kargs['index'] -> from 0 to .., index of sub-event Id
			return ids list, only for a recurrent event, just return the sub ones which match the 'masterId' '''
		eventRes = eval(kargs['res'])['events']['results']
		index = int(kargs['index'])
		ids = []
		for event in eventRes:
			if event.has_key('recurrenceOf') and event['recurrenceOf'] == kargs['masterId']:
				ids.append(event['uid'])
		return ids[index]
		
		
	def del_events(self, **kargs):
		'''kargs -> either 'params.calendarId' and 'ids', means delete all ids from 'ids' list
					or 'params.calendarId' and 'params.eventId'
		'''
		if kargs.has_key('ids'):
			ids = kargs['ids']
			del kargs['ids']
			for id in ids:
				kargs['params.eventId'] = id
				self.del_event(**kargs)
		else:
			print 'del a event'
			self.del_event(**kargs)
		
	def empty_event(self, **kargs):
		'''kargs['name'], params.startTime, params.endTime  '''
		get_id_h = {'name': kargs['name']}
		cal_ids = self.get_calendar_id_by_name(**get_id_h)
		
		report_event_h = {'params.calendarIds':cal_ids,'params.startTime': kargs['params.startTime'], 'params.endTime': kargs['params.endTime']}
		events_res = self.report_event(**report_event_h)
		
		original_ids_h = {'res': events_res}
		event_ids = self.get_oringinal_event_ids(**original_ids_h)
		
		del_events_h = {'params.calendarId':cal_ids[0], 'ids': event_ids}
		self.del_events(**del_events_h)
		
		return 'Empty events done'
	
	def birthday_startTime(self, **kargs):
		'''
			i.e. 
			(refer to ${birth day}	makeContactField	label=birthday	type=lzPersonal	value=19860608	primary=false)
			${birthday_startTime}	birthday_startTime	birthday=${birth day}
		'''
		return str(kargs['birthday']['value'])+'T000000'
	
	
	def empty_tasklist(self, **kargs):
		list_tasklist_params = {'params.calendarId':kargs['calendarId']}
		list_tasklist_res = self.list_tasklist(**list_tasklist_params)
		
		GHelper_params = {'res':list_tasklist_res, 'all':'true'}
		tasklist_id_list = self.GHelper.get_id_list_by_name(**GHelper_params)
		
		for id in tasklist_id_list:
			del_tasklist_params = {'params.calendarId':kargs['calendarId'], 'params.taskListId':id}
			self.del_tasklist(**del_tasklist_params)
		return 'All tasklist are deleted'
	
	def empty_todos(self, **kargs):
		''' kargs['name'] = ${common_from}${common_domain}'s main calendar'''
		calid = self.get_calendar_id_by_name(**kargs)
		list_task_h = {'params.calendarId': calid}
		list_task_res = self.list_task(**list_task_h)
		todo_list = eval(list_task_res)['toDos']['results']
		uid_k = {'res':todo_list, 'all':True}
		uid_list = self.GHelper.get_id_list_by_name(**uid_k)
		
		del_task_k = {'params.calendarId': calid}
		# del_task	params.calendarId=${cal ids}	params.toDoId=${created_uid}
		for uid in uid_list:
			del_task_k['params.toDoId'] = uid
			self.del_task(**del_task_k)
			print 'del '+str(uid)
		return 'empty_todos done for the calendar'
		


		
	
	# ---------------------------------------old func----------------------------------------------
	def get_cal_id_by_name(self, **kargs):
		res = self.list_calendar()
		result_list = utils.getCalendarIDListByName(kargs['name'], res)
		if len(result_list) == 0:
			raise Exception('Can not find calendar(name : %s) !'%kargs['name'])
		return result_list[0]

	
	def create_max_calendar(self,**kargs):
		if not kargs.has_key('calendarMax'):
			raise Exception('Missing calendarMax in parameters!')
		exceedNumber = int(kargs['calendarMax']) + 1
		for i in range(exceedNumber):
			try:
				kargs['name'] = 'testmax' + str(i)
				self.create_calendar(**kargs)
				print 'create number '+str(i)
			except Exception,ex:
				if (i == int(kargs['calendarMax'])): #to do:need to assert the error msg
					return 'One more than Max raise exception, case pass!'
				else:
					print 'number '+str(i)+' failed'
					raise ex
		raise Exception('Exceed the nested layer limitation %s! No error found in response.'%str(exceedNumber))	

	def check_event_by_summary(self, **kargs):
		#report event
		expectStr = ''
		if kargs.has_key('expectStr'):
			expectStr = kargs['expectStr']
			kargs.pop('expectStr')
		expectCnt = kargs['expectCnt']
		summary = kargs['summary']
		kargs.pop('expectCnt')
		kargs.pop('summary')
		#get all event content by summary
		report_res = self.report_event(**kargs)
		event_cont_list = utils.getEventContentBySummary(summary, report_res)
		
		if len(event_cont_list) != int(expectCnt):
			raise Exception('Expect count of event(summary=%s) is %s, but actually got %s'%(summary, expectCnt, len(event_cont_list)))
		
		if expectStr != '':
			expect_list = expectStr.split(',')
			for event_cont in event_cont_list:
				for expect in expect_list:
					if not expect in str(event_cont):
						raise Exception('Did not find "%s" in event content: %s'%(expect, str(event_cont)))
	
	def get_one_event_id(self, **kargs):
		summary = kargs['summary']
		kargs.pop('summary')
		report_res = self.report_event(**kargs)
		event_id_list = utils.getEventIDBySummary(summary, report_res)
		if len(event_id_list) == 0:
			raise Exception('Can not find any event with summary(%s), when get one event id.'%summary)
		return event_id_list[0]
		
	def get_master_id(self, **kargs):
		summary = kargs['summary']
		kargs.pop('summary')
		report_res = self.report_event(**kargs)
		master_id = utils.getEventMasterIDBySummary(summary, report_res)
		if None == master_id:
			raise Exception('Can not find master event id with summary(%s)!'%summary)
		return master_id
		
	def get_a_diff_event_id(self, **kargs):
		summary = kargs['summary']
		kargs.pop('summary')
		event_id = kargs['event_id']
		kargs.pop('event_id')
		report_res = self.report_event(**kargs)
		event_id_list = utils.getEventIDBySummary(summary, report_res)
		if len(event_id_list) == 0:
			raise Exception('Can not find any event with summary(%s), when get one event id.'%summary)
		for id in event_id_list:
			if id != event_id:
				return id
		raise Exception('Can not find any different event id!')
		
	def get_event_id_by_summary(self, **kargs):
		report_res = self.report_event(**kargs)
		summary = kargs['summary']
		event_id_list = utils.getEventIDBySummary(summary, report_res)
		return event_id_list
	
	

	
	def export_event(self, **kargs):
		url = kargs['url']	
		request = self.reqBuilder.buildSimpleReq('EVENT_EXPORT', True, True, **kargs)#you'd better input file name.
		data = {}
		data['r'] = request
		r = self.client.session.post(url,data)
		if 'error' in r.text:
			raise Exception('Error:'+r.text)
		else:
			return 'Events exported !'

			
	def create_event_negative(self, **kargs):
		try:
			self.create_event(**kargs)
		except Exception, e:
			if 'INTERNAL_ERROR' in str(e):
				pass
			else:
				raise Exception('Did not get expected error : ')
			

	def check_task_by_summary(self, **kargs):
		#report event
		expectStr = ''
		expectCnt = kargs['expectCnt']
		summary = kargs['summary']
		kargs.pop('expectCnt')
		#get all event content by summary
		report_res = self.list_task(**kargs)
		task_cont_list = utils.getTaskContentBySummary(summary, report_res)
		
		if len(task_cont_list) != int(expectCnt):
			raise Exception('Expect count of task(summary=%s) is %s, but actually got %s'%(summary, expectCnt, len(task_cont_list)))
		
		if kargs.has_key('expectStr'):
			expectStr = kargs['expectStr']
			kargs.pop('expectStr')
			expect_list = expectStr.split(',')
			for task_cont in task_cont_list:
				for expect in expect_list:
					if not expect in task_cont:
						raise Exception('Did not find "%s" in task content: %s'%(expect, task_cont))
			
			
	def get_task_id_by_summary(self, **kargs):
		res = self.list_task(**kargs)
		result_list = utils.getTaskIDBySummary(kargs['summary'], res)
		if len(result_list) == 0:
			raise Exception('Can not find task(summary : %s) !'%kargs['summary'])
		return result_list[0]

	def empty_task(self, **kargs):
		report_res = self.list_task(**kargs)
		id_list = utils.getTaskIDList(report_res)
		for each_id in id_list:
			kargs['id'] = each_id
			try:
				self.del_task(**kargs)
			except Exception, e:
				print str(e)

	def check_tasklist_by_name(self, **kargs):
		#report event
		expectStr = ''
		expectCnt = kargs['expectCnt']
		name = kargs['name']
		kargs.pop('expectCnt')
		#get all group by name
		report_res = self.list_tasklist(**kargs)
		group_id_list = utils.getTaskListIDByName(name, report_res)
		
		if len(group_id_list) != int(expectCnt):
			raise Exception('Expect count of group(name=%s) is %s, but actually got %s'%(name, expectCnt, len(group_id_list)))

		
	def get_tasklist_id_by_name(self, **kargs):
		res = self.list_tasklist(**kargs)
		result_list = utils.getTaskListIDByName(kargs['name'], res)
		if len(result_list) == 0:
			raise Exception('Can not find group(name : %s) !'%kargs['name'])
		return result_list[0]
		
	def empty_taskgroup(self, **kargs):
		report_res = self.list_tasklist(**kargs)
		id_list = utils.getTaskListIDList(report_res)
		for each_id in id_list:
			kargs['id'] = each_id
			try:
				self.del_taskgroup(**kargs)
			except Exception, e:
				print str(e)	

	def export_task(self, **kargs):
		url = kargs['url']	
		request = self.reqBuilder.buildSimpleReq('TASK_EXPORT', True, True, **kargs)#you'd better input file name.
		data = {}
		data['r'] = request
		r = self.client.session.post(url,data)
		if 'error' in r.text:
			raise Exception('Error:'+r.text)
		else:
			return 'Tasks exported !'


	def share_group_no_task(self, **kargs):
		try:
			resp = self.share_group_by_email(**kargs)
		except Exception, e:
			if ('INVALID_REQUEST' in str(e)) and ('calendar.task.noTaskFound' in str(e)):
				return
		raise Exception('Should return INVALID_REQUEST exception, but actually not.')


	def check_report_event(self, **kargs):
		'''
		this is used only for report_event testing
		'''
		#report event
		expectStr = ''
		expectCnt = kargs['expectCnt']
		kargs.pop('expectCnt')
		if kargs.has_key('expectStr'):
			expectStr = kargs['expectStr']
			kargs.pop('expectStr')
		#get all event content by summary
		report_res = self.report_event(**kargs)
		event_list = json.loads(report_res)['events']['results']
		if len(event_list) != int(expectCnt):
			raise Exception('Report event doesn\'t work well! Expect count of events is %s, but actually got %s'%(expectCnt, len(event_list)))
		
		if expectStr != '':
			expect_list = str(expectStr).split(',')
			for event_cont in event_list:
				for expect in expect_list:
					if not expect in str(event_cont):
						raise Exception('Report event doesn\'t work well! Did not find "%s" in event content: %s'%(expect, str(event_cont)))
		
	
	def check_report_task(self, **kargs):
		'''
		this is used only for report_todos testing
		'''
		#report event
		expectStr = ''
		expectCnt = kargs['expectCnt']
		kargs.pop('expectCnt')
		if kargs.has_key('expectStr'):
			expectStr = kargs['expectStr']
			kargs.pop('expectStr')
		#get all event content by summary
		report_res = self.list_task(**kargs)
		task_list = json.loads(report_res)['toDos']['results']
		if len(task_list) != int(expectCnt):
			raise Exception('Report task doesn\'t work well! Expect count of tasks is %s, but actually got %s'%(expectCnt, len(task_list)))
		
		if expectStr != '':
			expect_list = str(expectStr).split(',')
			for task_cont in task_list:
				for expect in expect_list:
					if not expect in str(task_cont):
						raise Exception('Report task doesn\'t work well! Did not find "%s" in task content: %s'%(expect, str(task_cont)))		

	def make_attendee(self, **kargs):
		return kargs
		
	def get_event_default_startMillis(self):
		return int(time.mktime(datetime.datetime.strptime('20190930T093000', '%Y%m%dT%H%M%S').timetuple()))
	
	def get_event_default_endMillis(self):
		return int(time.mktime(datetime.datetime.strptime('20190930T100000', '%Y%m%dT%H%M%S').timetuple()))

	def get_event_default_untilMillis(self):
		return int(time.mktime(datetime.datetime.strptime('20191130T235959', '%Y%m%dT%H%M%S').timetuple()))
		
	def get_event_default_starttime(self):
		return '20180930T013000'
		
	def get_event_default_endtime(self):
		return '20201130T235959'
		
	def create_event_1(self, **kargs):
		#return uid(master id) after create_event
		try:
			res = self.create_event(**kargs)
			result = json.loads(res)
			return result['uid']
		except Exception, e:
			raise e
	
# newfile = open('E:\\Repositaries\\robot\\workspace\\Libs\\tmp.txt','w')
# newfile.write(res.read()) # str(re.findall('.*(<todo summary.*/todo>).*',TaskResp))
# newfile.close()