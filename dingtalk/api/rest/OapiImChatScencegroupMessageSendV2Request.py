'''
Created by auto_sdk on 2021.11.22
'''
from dingtalk.api.base import RestApi
class OapiImChatScencegroupMessageSendV2Request(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.at_mobiles = None
		self.at_union_ids = None
		self.at_users = None
		self.is_at_all = None
		self.msg_media_id_param_map = None
		self.msg_param_map = None
		self.msg_template_id = None
		self.receiver_mobiles = None
		self.receiver_union_ids = None
		self.receiver_user_ids = None
		self.robot_code = None
		self.target_open_conversation_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.scencegroup.message.send_v2'
