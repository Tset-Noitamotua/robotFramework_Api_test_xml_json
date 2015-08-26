import sys, os
sys.path.append(os.path.join('..', 'util'))
from ImpLibs import consts, utils, reqbuilder
from Base import Base

class Calendar(Base):
	'''
	include all calendar APIs
	'''
	def __init__(self, url):
		Base.__init__(self, url)
		
	def list_calendar(self, **kargs):
		try:
			response = self.request_send('CALENDAR_LIST', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_LIST failed - %s'%str(e))		
		
	def create_calendar(self, **kargs):
		'''
		input:
			name
			color : [0..14], default is 9
		'''
		try:
			response = self.request_send('CALENDAR_CREATE', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_CREATE failed - %s'%str(e))		
		
	def del_calendar(self, **kargs):		
		try:
			response = self.request_send('CALENDAR_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_DEL failed - %s'%str(e))		
		
	def empty_calendar(self, **kargs):
		try:
			response = self.request_send('CALENDAR_EMPTY', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_EMPTY failed - %s'%str(e))	
		
	def rename_calendar(self, **kargs):
		try:
			response = self.request_send('CALENDAR_RENAME', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_RENAME failed - %s'%str(e))	

	def set_color_for_calendar(self, **kargs):
		try:
			response = self.request_send('CALENDAR_SETCOLOR', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_SETCOLOR failed - %s'%str(e))
			
	def set_visible_for_calendar(self, **kargs):
		try:
			response = self.request_send('CALENDAR_SETVISIBLE', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_SETVISIBLE failed - %s'%str(e))

	def get_access_list(self, **kargs):
		try:
			response = self.request_send('CALENDAR_GET_ACCESSLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_GET_ACCESSLIST failed - %s'%str(e))
		
	def set_access_list(self, **kargs):
		try:
			response = self.request_send('CALENDAR_SET_ACCESSLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_SET_ACCESSLIST failed - %s'%str(e))	
		
	def report_event(self, **kargs):
		try:
			response = self.request_send('EVENT_REPORT', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_REPORT failed - %s'%str(e))	
	
	def read_event(self, **kargs):
		try:
			response = self.request_send('EVENT_READ', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_READ - %s'%str(e))	

	def del_event(self, **kargs):
		try:
			response = self.request_send('EVENT_DEL', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_DEL failed - %s'%str(e))	

	def create_event(self, **kargs):
		try:
			response = self.request_send('EVENT_CREATE', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_CREATE failed - %s'%str(e))					
			
	def update_event(self, **kargs):
		try:
			response = self.request_send('EVENT_UPDATE', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_UPDATE failed - %s'%str(e))		
			
	def event_send_invite(self, **kargs):
		'''params.notifyType= CREATE_EVENT, UPDATE_EVENT, CANCEL_EVENT '''
		try:
			response = self.request_send('EVENT_SEND_INVITE', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_SEND_INVITE failed - %s'%str(e))	
	
	def attendee_update_event_rsvp(self, **kargs):
		try:
			response = self.request_send('RSVP_UPDATE', **kargs)
			return response
		except Exception, e:
			raise Exception('RSVP_UPDATE failed - %s'%str(e))	
	
	
	
	
	def subscribe_calendar(self, **kargs):
		try:
			response = self.request_send('SUBSCRIBE_CALENDAR', **kargs)
			return response
		except Exception, e:
			raise Exception('SUBSCRIBE_CALENDAR failed - %s'%str(e))		
	
	def list_subscribed(self, **kargs):
		try:
			response = self.request_send('LIST_SUBSCRIBED', **kargs)
			return response
		except Exception, e:
			raise Exception('LIST_SUBSCRIBED failed - %s'%str(e))
			
	def copy_event(self, **kargs):
		try:
			response = self.request_send('EVENT_COPY', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_COPY failed - %s'%str(e))
			
	def list_tasklist(self, **kargs):
		try:
			response = self.request_send('LIST_TASKLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('LIST_TASKLIST failed - %s'%str(e))			
			
	def create_tasklist(self, **kargs):
		try:
			response = self.request_send('CREATE_TASKLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('CREATE_TASKLIST failed - %s'%str(e))
			
	def del_tasklist(self, **kargs):
		try:
			response = self.request_send('DEL_TASKLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('DEL_TASKLIST failed - %s'%str(e))	
		
	def update_tasklist(self, **kargs):
		try:
			response = self.request_send('UPDATE_TASKLIST', **kargs)
			return response
		except Exception, e:
			raise Exception('UPDATE_TASKLIST failed - %s'%str(e))	
			
	def share_tasklist_by_mail(self, **kargs):
		try:
			response = self.request_send('SHARE_TASKLIST_BY_MAIL', **kargs)
			return response
		except Exception, e:
			raise Exception('SHARE_TASKLIST_BY_MAIL failed - %s'%str(e))
			
	def list_task(self, **kargs):
		try:
			response = self.request_send('TODO_REPORT', **kargs)
			return response
		except Exception, e:
			raise Exception('TODO_REPORT failed - %s'%str(e))	
		
	def create_task(self, **kargs):
		try:
			response = self.request_send('TODO_CREATE', **kargs)
			return response
		except Exception, e:
			raise Exception('TODO_CREATE failed - %s'%str(e))

	def update_task(self, **kargs):
		try:
			response = self.request_send('TODO_UPDATE', **kargs)
			return response
		except Exception, e:
			raise Exception('TODO_UPDATE failed - %s'%str(e))
			
			
	def del_task(self, **kargs):
		try:
			response = self.request_send('DEL_TODO', **kargs)
			return response
		except Exception, e:
			raise Exception('DEL_TODO failed - %s'%str(e))		
			
	def move_task(self, **kargs):
		try:
			response = self.request_send('TODO_MOVE', **kargs)
			return response
		except Exception, e:
			raise Exception('TODO_MOVE failed - %s'%str(e))		

	def import_event(self, **kargs):
		try:
			response = self.request_send('EVENT_IMPORT', **kargs)
			return response
		except Exception, e:
			raise Exception('EVENT_IMPORT failed - %s'%str(e))	

	def calendar_preference_load(self, **kargs):
		try:
			response = self.request_send('CALENDAR_PREFERENCE_LOAD', **kargs)
			return response
		except Exception, e:
			raise Exception('CALENDAR_PREFERENCE_LOAD failed - %s'%str(e))	
			
			
			
			
			

# ------------------------------old func-------------------------

	
			
	def share_calendar(self, **kargs):
		try:
			response = self.request_send('CALENAR_SHARE', **kargs)
			return response
		except Exception, e:
			raise Exception('Share calendar	failed - %s'%str(e))		
	
	def share_calendar_allow_anyone(self, **kargs):
		try:
			response = self.request_send('CALENDAR_SHARE_ALLOW_ANYONE', **kargs)
			return response
		except Exception, e:
			raise Exception('Share calendar	failed - %s'%str(e))
				
	# def create_task_with_alarm(self, **kargs):
		# try:
			# response = self.request_send('CREATE_TASK', **kargs)
			# return response
		# except Exception, e:
			# raise Exception('Create task failed - %s'%str(e))
			
	# def create_task_no_alarm(self, **kargs):
		# try:
			# response = self.request_send('CREATE_TASK_NO_ALARM', **kargs)
			# return response
		# except Exception, e:
			# raise Exception('Create task(no alarm) failed - %s'%str(e))
	
	
			
	def update_task_with_alarm(self, **kargs):
		try:
			response = self.request_send('UPDATE_TODO', **kargs)
			return response
		except Exception, e:
			raise Exception('Update task failed - %s'%str(e))
			
	def update_task_no_alarm(self, **kargs):
		try:
			response = self.request_send('UPDATE_TODO_NO_ALARM', **kargs)
			return response
		except Exception, e:
			raise Exception('Update task(no alarm) failed - %s'%str(e))
			
	def import_task(self, **kargs):
		try:
			response = self.request_send('EVENT_IMPORT', **kargs)
			return response
		except Exception, e:
			raise Exception('Import events failed - %s'%str(e))	
			
	