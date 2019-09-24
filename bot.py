from config import Config
from proxy_manager import update_proxy
import telepot
from telepot.loop import MessageLoop

class Bot:
	def __init__(self):
		self.init_bot()

	def init_bot(self):
		
		config = Config()

		if config.read('use_proxy'):
			self.set_proxy(config.read('proxy_url'))

		self.bot = telepot.Bot(config.read("bot_token"))

		# check if connection established
		if not self.check_connection(self.bot):
			if config.read('use_proxy'):
				# search for new proxy
				proxy_url = update_proxy()
				if proxy_url == '':
					# couldn't find a good proxy
					return
				self.set_proxy(proxy_url)
	
	def set_proxy(self, proxy):
		telepot.api.set_proxy(proxy)

	def check_connection(self, bot):
		try:
			bot.getMe()
			return True
		except:
			return False

	def send_message(self, chat_id, msg, msg_id=None, format=None):
		self.bot.sendMessage(chat_id, msg, reply_to_message_id=msg_id, parse_mode=format)

	def send_audio(self, chat_id, audio):
		self.bot.sendAudio(chat_id, audio)
	
	def send_video(self, chat_id, video):
		self.bot.sendVideo(chat_id, video)

	def send_master_message(self, msg):
		self.send_message(Config().read('master_chat_id'), msg)
	
	def listen(self, handler):
		MessageLoop(self.bot, handler).run_as_thread()
