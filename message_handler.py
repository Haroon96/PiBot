from bot import Bot
import time
from config import Config
from controller import interpret
from telepot.loop import MessageLoop

def handler(message):
	text = message['text']
	chat_id = message['chat']['id']
	interpret(text, chat_id)

def main():
	bot = Bot()

	bot.send_master_message('Booted!')
	# start listening for new messages

	MessageLoop(bot.bot, handler).run_as_thread()

	while 1:
		time.sleep(10)
	
if __name__ == '__main__':
	main()