from bot import Bot
import time
from telepot.loop import MessageLoop
from config import Config
from controller import interpret

def handle(message):
	text = message['text']
	chat_id = message['chat']['id']
	interpret(text, chat_id)

def main():
	bot = Bot()

	# start listening for new messages
	MessageLoop(bot.bot, handle).run_as_thread()

	while 1:
		time.sleep(10)
	
if __name__ == '__main__':
	main()

