HostPort='http://172.20.0.78:8080/kiwi-octane-2.1.19'
login_url=HostPort + '/bin/auth'
# HostPort='http://172.20.0.78:8080/kiwi-octane/bin/auth'
common_url=HostPort + '/json'
common_domain='@openwave.com'
common_to='webtop6'
common_from='webtop20'
mail_password='p'
mail_subject='test'
mail_body='Mail Body'

resource_load = HostPort+'/bin'
resource_upload = resource_load + '?r=resource.upload'

# common_upload_url= HostPort + '/http/upload?' # will be removed, works now for xml
# mail_get_attach_url=HostPort + '/http/viewattachment?&accountId&folder=%s&uid=%s&part=%s'
mail_vieweml=HostPort + '/bin'
# contact_export=HostPort + '/http/download/' # will be removed, works now for xml
resource_load = HostPort+'/bin' # latest upload/download Json will use
current_user_info_fields=['mail', 'blockedSenderSettings', 'mailForwarding', 'mailSignature', 'addressBook', 'mailFilter', 'contacts', 'allowedSenderSettings', 'vacationMessage', 'collectedAddress', 'externalMailAccount', 'trustedSender', 'user', 'calendar']
default_addressbook_name='Default'
auto_complete_addressbook_name='Auto-complete'
default_from_cal_name=common_from + common_domain + '\'s main calendar' #used for birthday event
max_autocmpltcontact=20
max_autocollect_count=20
max_addressbook_count=8