HostPort='http://172.20.0.78:8080/kiwi-octane-2.1.19'
login_url=HostPort + '/bin/auth'
common_url=HostPort + '/json'
common_domain='@openwave.com'
common_to='webtop2'
common_from='webtop1'
mail_password='p'
mail_subject='test'
mail_body='Mail Body'
mail_cc='webtop3'
mail_bcc='webtop4'
resource_load = HostPort+'/bin'
resource_upload = resource_load + '?r=resource.upload'
# file_upload = resource_load + '?r=fileUpload.upload'

common_upload_url=HostPort + '/bin?'
mail_faceImg=HostPort + '/html/rte/resources/images/1.gif'
# mail_get_attach_url=HostPort + '/http/viewattachment?&accountId&folder=%s&uid=%s&part=%s'
mail_vieweml=HostPort + '/bin'
# contact_export=HostPort + '/http/download/'
inbox_folder = 'Inbox'
draft_folder = 'Drafts'
sent_mail_folder = 'SentMail'
spam_folder = 'Spam'
trash_folder = 'Trash'

max_signature=10
embedImg='&amp;#128516;&lt;br&gt;'
folder_nested_depth=30
token_expiry_hour=24
max_external_acc=12
language=['zh_CN', 'zh_TW', 'ja_JP', 'it_IT', 'fr_FR', 'en_US']
default_addressbook_name='Default'
max_send_size=1024    # K
# sent_mail_folder='SentMail'    # fusion : SentMail | tpn : Sent
# spam_folder='Spam'    # fusion:Spam | tpv: spam
# draft_folder='drafts'
# trash_folder='trash'
mail_deliver_receipt_msg='Mail System Delivery Report'    # tpv:Delivery Status Notification|fusion:Mail System Delivery Report
default_timezone='Etc/GMT'
timezone_group_1=['GMT -11:00', 'GMT -10:00', 'GMT -09:30', 'GMT -09:00', 'GMT -08:00', 'GMT -07:00']
timezone_group_2=['GMT -06:00', 'GMT -05:00', 'GMT -04:30']                     
timezone_group_3=['GMT -04:00', 'GMT -03:30', 'GMT -03:00', 'GMT -02:00', 'GMT -01:00']        
timezone_group_4=['GMT +00:00', 'GMT +01:00', 'GMT +02:00']
timezone_group_5=['GMT +03:00', 'GMT +03:30', 'GMT +04:00', 'GMT +05:00', 'GMT +05:30', 'GMT +05:45']           
timezone_group_6=['GMT +06:00', 'GMT +06:30', 'GMT +07:00', 'GMT +08:00', 'GMT +08:45']                 
timezone_group_7=['GMT +09:00', 'GMT +09:30', 'GMT +10:00', 'GMT +11:00', 'GMT +11:30', 'GMT +12:00', 'GMT +12:45', 'GMT +13:00', 'GMT +14:00']     
read_receipt_str='Return Receipt' 
deliver_receipt_subject='Mail System Delivery Report' 
external_domain='test3.com'
external_user='vivian1'        
