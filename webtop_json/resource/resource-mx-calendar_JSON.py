localhost = '172.20.0.78'
HostPort='http://%s:8080/kiwi-octane-2.1.19'%localhost
login_url=HostPort + '/bin/auth'
common_url=HostPort + '/json'
common_domain='@openwave.com'
common_to='webtop8'
common_from='webtop7'
mail_password='p'

resource_load = HostPort+'/bin'
resource_upload = resource_load + '?r=resource.upload'



# common_upload_url=HostPort + '/http/upload?token=%s&sessionId=%s'
# mail_get_attach_url=HostPort + '/http/viewattachment?&accountId&folder=%s&uid=%s&part=%s'
# contact_export=HostPort + '/http/download/'
max_cal=9
sent_mail_folder='SentMail'    # fusion : SentMail | tpn : Sent
spam_folder='Spam'    # fusion:Spam | tpv: spam
mail_deliver_receipt_msg='Mail System Delivery Report'    # tpv:Delivery Status Notification|fusion:Mail System Delivery Report
default_timezone='Etc/GMT'
default_cal_name=common_from + common_domain + '\'s main calendar'
default_cal_name_to=common_to + common_domain + '\'s main calendar'
event_category=['general', 'invite', 'work', 'school', 'red', 'yellow', 'green', 'birthday', 'anniversary', 'date', 'vacation', 'fun', 'bills', 'phone','doctor', 'flag', 'pet', 'sport']
event_daylist=['FR', 'MO', 'SA', 'SU', 'TH', 'TU', 'WE']
local_timezone='America/Vancouver'
# local_timezone='Asia/Shanghai'
current_user_info_fields=['mail', 'blockedSenderSettings', 'mailForwarding', 'mailSignature', 'addressBook', 'mailFilter', 'contacts', 'allowedSenderSettings', 'vacationMessage', 'collectedAddress', 'externalMailAccount', 'trustedSender', 'user', 'calendar']

