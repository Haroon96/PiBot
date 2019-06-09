import time
from controller import interpret
from bot import Bot
from config import Config

def handler(message):
	chat_id = message['chat']['id']
	interpret(message, chat_id)

def main():
	bot = Bot()

	bot.send_master_message('Booted!')
	# start listening for new messages
	bot.listen(handler)

	while 1:
		time.sleep(10)
	
if __name__ == '__main__':
	main()
