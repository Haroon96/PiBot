import telepot
import sys
import os
from proxy import get_proxy

def check_args(args):
	if len(args) <= 1:
		print("No arguments specified")
		return False
	return True

def get_base_path():
	path = os.path.realpath(__file__)
	path = path[:path.rindex("/")]	
	return path

def load_config():
	''' TODO: check for exceptions here '''
	chat_id = open(get_base_path() + "/chat_id").read().strip()
	token = open(get_base_path() + "/token").read().strip()
	return chat_id, token

def form_message(args):
	return " ".join(args[1:])

def create_bot(token):	
	telepot.api.set_proxy(get_proxy())
	return telepot.Bot(token)

def send_message(message):
	chat_id, token = load_config()
	create_bot(token).sendMessage(chat_id, message)

def main():
	if check_args(sys.argv):
		message = form_message(sys.argv)
		send_message(message)

if __name__ == "__main__":
	main()
