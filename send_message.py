import telepot
import sys
from proxy import get_proxy

def check_args(args):
	if len(args) <= 1:
		print("No arguments specified")
		return False
	return True

def load_config():
	''' TODO: check for exceptions here '''
	chat_id = open("chat_id").read().strip()
	token = open("token").read().strip()
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
